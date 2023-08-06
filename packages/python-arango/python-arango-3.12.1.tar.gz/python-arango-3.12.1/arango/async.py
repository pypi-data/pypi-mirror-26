from __future__ import absolute_import, unicode_literals

from arango.collections import Collection
from arango.connection import Connection
from arango.utils import HTTP_OK
from arango.exceptions import (
    AsyncExecuteError,
    AsyncJobCancelError,
    AsyncJobStatusError,
    AsyncJobResultError,
    AsyncJobClearError
)
from arango.graph import Graph
from arango.aql import AQL


class AsyncExecution(Connection):
    """ArangoDB asynchronous execution.

    API requests via this class are placed in a server-side in-memory task
    queue and executed asynchronously in a fire-and-forget style.

    :param connection: ArangoDB database connection
    :type connection: arango.connection.Connection
    :param return_result: if ``True``, an :class:`arango.async.AsyncJob`
        instance (which holds the result of the request) is returned each
        time an API request is queued, otherwise ``None`` is returned
    :type return_result: bool

    .. warning::
        Asynchronous execution is currently an experimental feature and is not
        thread-safe.
    """

    def __init__(self, connection, return_result=True):
        super(AsyncExecution, self).__init__(
            protocol=connection.protocol,
            host=connection.host,
            port=connection.port,
            username=connection.username,
            password=connection.password,
            http_client=connection.http_client,
            database=connection.database,
            enable_logging=connection.logging_enabled
        )
        self._return_result = return_result
        self._aql = AQL(self)
        self._type = 'async'

    def __repr__(self):
        return '<ArangoDB asynchronous execution>'

    def handle_request(self, request, handler):
        """Handle the incoming request and response handler.

        :param request: the API request to be placed in the server-side queue
        :type request: arango.request.Request
        :param handler: the response handler
        :type handler: callable
        :returns: the async job or None
        :rtype: arango.async.AsyncJob
        :raises arango.exceptions.AsyncExecuteError: if the async request
            cannot be executed
        """
        if self._return_result:
            request.headers['x-arango-async'] = 'store'
        else:
            request.headers['x-arango-async'] = 'true'

        res = getattr(self, request.method)(**request.kwargs)
        if res.status_code not in HTTP_OK:
            raise AsyncExecuteError(res)
        if self._return_result:
            return AsyncJob(self, res.headers['x-arango-async-id'], handler)

    @property
    def aql(self):
        """Return the AQL object tailored for asynchronous execution.

        API requests via the returned query object are placed in a server-side
        in-memory task queue and executed asynchronously in a fire-and-forget
        style.

        :returns: ArangoDB query object
        :rtype: arango.query.AQL
        """
        return self._aql

    def collection(self, name):
        """Return a collection object tailored for asynchronous execution.

        API requests via the returned collection object are placed in a
        server-side in-memory task queue and executed asynchronously in
        a fire-and-forget style.

        :param name: the name of the collection
        :type name: str | unicode
        :returns: the collection object
        :rtype: arango.collections.Collection
        """
        return Collection(self, name)

    def graph(self, name):
        """Return a graph object tailored for asynchronous execution.

        API requests via the returned graph object are placed in a server-side
        in-memory task queue and executed asynchronously in a fire-and-forget
        style.

        :param name: the name of the graph
        :type name: str | unicode
        :returns: the graph object
        :rtype: arango.graph.Graph
        """
        return Graph(self, name)


class AsyncJob(object):
    """ArangoDB async job which holds the result of an API request.

    An async job tracks the status of a queued API request and its result.

    :param connection: ArangoDB database connection
    :type connection: arango.connection.Connection
    :param job_id: the ID of the async job
    :type job_id: str | unicode
    :param handler: the response handler
    :type handler: callable
    """

    def __init__(self, connection, job_id, handler):
        self._conn = connection
        self._id = job_id
        self._handler = handler

    def __repr__(self):
        return '<ArangoDB asynchronous job {}>'.format(self._id)

    @property
    def id(self):
        """Return the ID of the async job.

        :returns: the ID of the async job
        :rtype: str | unicode
        """
        return self._id

    def status(self):
        """Return the status of the async job from the server.

        :returns: the status of the async job, which can be ``"pending"`` (the
            job is still in the queue), ``"done"`` (the job finished or raised
            an exception)
        :rtype: str | unicode
        :raises arango.exceptions.AsyncJobStatusError: if the status of the
            async job cannot be retrieved from the server
        """
        res = self._conn.get('/_api/job/{}'.format(self.id))
        if res.status_code == 204:
            return 'pending'
        elif res.status_code in HTTP_OK:
            return 'done'
        elif res.status_code == 404:
            raise AsyncJobStatusError(res, 'Job {} missing'.format(self.id))
        else:
            raise AsyncJobStatusError(res)

    def result(self):
        """Return the result of the async job if available.

        :returns: the result or the exception from the async job
        :rtype: object
        :raises arango.exceptions.AsyncJobResultError: if the result of the
            async job cannot be retrieved from the server

        .. note::
            An async job result will automatically be cleared from the server
            once fetched and will *not* be available in subsequent calls.
        """
        res = self._conn.put('/_api/job/{}'.format(self._id))
        if ('X-Arango-Async-Id' in res.headers
                or 'x-arango-async-id' in res.headers):
            try:
                result = self._handler(res)
            except Exception as error:
                return error
            else:
                return result
        elif res.status_code == 204:
            raise AsyncJobResultError(res, 'Job {} not done'.format(self._id))
        elif res.status_code == 404:
            raise AsyncJobResultError(res, 'Job {} missing'.format(self._id))
        else:
            raise AsyncJobResultError(res)

    def cancel(self, ignore_missing=False):  # pragma: no cover
        """Cancel the async job if it is still pending.

        :param ignore_missing: ignore missing async jobs
        :type ignore_missing: bool
        :returns: ``True`` if the job was cancelled successfully, ``False`` if
            the job was not found but **ignore_missing** was set to ``True``
        :rtype: bool
        :raises arango.exceptions.AsyncJobCancelError: if the async job cannot
            be cancelled

        .. note::
            An async job cannot be cancelled once it is taken out of the queue
            (i.e. started, finished or cancelled).
        """
        res = self._conn.put('/_api/job/{}/cancel'.format(self._id))
        if res.status_code == 200:
            return True
        elif res.status_code == 404:
            if ignore_missing:
                return False
            raise AsyncJobCancelError(res, 'Job {} missing'.format(self._id))
        else:
            raise AsyncJobCancelError(res)

    def clear(self, ignore_missing=False):
        """Delete the result of the job from the server.

        :param ignore_missing: ignore missing async jobs
        :type ignore_missing: bool
        :returns: ``True`` if the result was deleted successfully, ``False``
            if the job was not found but **ignore_missing** was set to ``True``
        :rtype: bool
        :raises arango.exceptions.AsyncJobClearError: if the result of the
            async job cannot be delete from the server
        """
        res = self._conn.delete('/_api/job/{}'.format(self._id))
        if res.status_code in HTTP_OK:
            return True
        elif res.status_code == 404:
            if ignore_missing:
                return False
            raise AsyncJobClearError(res, 'Job {} missing'.format(self._id))
        else:
            raise AsyncJobClearError(res)
