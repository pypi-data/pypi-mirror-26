from __future__ import absolute_import, unicode_literals

from uuid import UUID

import pytest

from arango import ArangoClient
from arango.aql import AQL
from arango.collections import Collection
from arango.exceptions import (
    DocumentRevisionError,
    DocumentInsertError,
    BatchExecuteError
)
from arango.graph import Graph

from .utils import (
    generate_db_name,
    generate_col_name,
)

arango_client = ArangoClient()
db_name = generate_db_name()
db = arango_client.create_database(db_name)
bad_db_name = generate_db_name()
bad_db = arango_client.db(bad_db_name)
col_name = generate_col_name()
col = db.create_collection(col_name)


def teardown_module(*_):
    arango_client.delete_database(db_name, ignore_missing=True)


def setup_function(*_):
    col.truncate()


def test_init():
    batch = db.batch()
    assert batch.type == 'batch'
    assert 'ArangoDB batch execution {}'.format(batch.id) in repr(batch)
    assert isinstance(batch.aql, AQL)
    assert isinstance(batch.graph('test'), Graph)
    assert isinstance(batch.collection('test'), Collection)


def test_batch_job_properties():
    with db.batch(return_result=True) as batch:
        batch_col = batch.collection(col_name)
        job = batch_col.insert({'_key': '1', 'val': 1})

    assert isinstance(job.id, UUID)
    assert 'ArangoDB batch job {}'.format(job.id) in repr(job)


def test_batch_empty_commit():
    batch = db.batch(return_result=True)
    assert batch.commit() is None


def test_batch_invalid_commit():
    assert len(col) == 0
    batch = bad_db.batch(return_result=True)
    batch_col = batch.collection(col_name)
    batch_col.insert({'_key': '1', 'val': 1})
    batch_col.insert({'_key': '2', 'val': 2})
    batch_col.insert({'_key': '2', 'val': 3})

    with pytest.raises(BatchExecuteError):
        batch.commit()
    assert len(col) == 0


def test_batch_insert_context_manager_with_result():
    assert len(col) == 0
    with db.batch(return_result=True) as batch:
        batch_col = batch.collection(col_name)
        job1 = batch_col.insert({'_key': '1', 'val': 1})
        job2 = batch_col.insert({'_key': '2', 'val': 2})
        job3 = batch_col.insert({'_key': '2', 'val': 3})
        job4 = batch_col.get(key='2', rev='9999')

    assert len(col) == 2
    assert col['1']['val'] == 1
    assert col['2']['val'] == 2

    assert job1.status() == 'done'
    assert job1.result()['_key'] == '1'

    assert job2.status() == 'done'
    assert job2.result()['_key'] == '2'

    assert job3.status() == 'error'
    assert isinstance(job3.result(), DocumentInsertError)

    assert job4.status() == 'error'
    assert isinstance(job4.result(), DocumentRevisionError)


def test_batch_insert_context_manager_without_result():
    assert len(col) == 0
    with db.batch(return_result=False) as batch:
        batch_col = batch.collection(col_name)
        job1 = batch_col.insert({'_key': '1', 'val': 1})
        job2 = batch_col.insert({'_key': '2', 'val': 2})
        job3 = batch_col.insert({'_key': '2', 'val': 3})
    assert len(col) == 2
    assert col['1']['val'] == 1
    assert col['2']['val'] == 2
    assert job1 is None
    assert job2 is None
    assert job3 is None


def test_batch_insert_context_manager_commit_on_error():
    assert len(col) == 0
    try:
        with db.batch(return_result=True, commit_on_error=True) as batch:
            batch_col = batch.collection(col_name)
            job1 = batch_col.insert({'_key': '1', 'val': 1})
            raise ValueError('Error!')
    except ValueError:
        assert col['1']['val'] == 1
        assert job1.status() == 'done'
        assert job1.result()['_key'] == '1'


def test_batch_insert_context_manager_no_commit_on_error():
    assert len(col) == 0
    try:
        with db.batch(return_result=True, commit_on_error=False) as batch:
            batch_col = batch.collection(col_name)
            job1 = batch_col.insert({'_key': '1', 'val': 1})
            raise ValueError('Error!')
    except ValueError:
        assert len(col) == 0
        assert job1.status() == 'pending'
        assert job1.result() is None


def test_batch_insert_no_context_manager_with_result():
    assert len(col) == 0
    batch = db.batch(return_result=True)
    batch_col = batch.collection(col_name)
    job1 = batch_col.insert({'_key': '1', 'val': 1})
    job2 = batch_col.insert({'_key': '2', 'val': 2})
    job3 = batch_col.insert({'_key': '2', 'val': 3})

    assert len(col) == 0
    assert job1.status() == 'pending'
    assert job1.result() is None

    assert job2.status() == 'pending'
    assert job2.result() is None

    assert job3.status() == 'pending'
    assert job3.result() is None

    batch.commit()
    assert len(col) == 2
    assert col['1']['val'] == 1
    assert col['2']['val'] == 2

    assert job1.status() == 'done'
    assert job1.result()['_key'] == '1'

    assert job2.status() == 'done'
    assert job2.result()['_key'] == '2'

    assert job3.status() == 'error'
    assert isinstance(job3.result(), DocumentInsertError)


def test_batch_insert_no_context_manager_without_result():
    assert len(col) == 0
    batch = db.batch(return_result=False)
    batch_col = batch.collection(col_name)
    job1 = batch_col.insert({'_key': '1', 'val': 1})
    job2 = batch_col.insert({'_key': '2', 'val': 2})
    job3 = batch_col.insert({'_key': '2', 'val': 3})

    assert job1 is None
    assert job2 is None
    assert job3 is None

    batch.commit()
    assert len(col) == 2
    assert col['1']['val'] == 1
    assert col['2']['val'] == 2


def test_batch_query_context_manager_with_result():
    with db.batch(return_result=True, commit_on_error=False) as batch:
        job1 = batch.collection(col_name).import_bulk([
            {'_key': '1', 'val': 1},
            {'_key': '2', 'val': 2},
            {'_key': '3', 'val': 3},
        ])
        job2 = batch.aql.execute(
            'FOR d IN {} RETURN d'.format(col_name),
            count=True,
            batch_size=1,
            ttl=10,
            optimizer_rules=['+all']
        )
        job3 = batch.aql.execute(
            'FOR d IN {} FILTER d.val == @value RETURN d'.format(col_name),
            bind_vars={'value': 1},
            count=True
        )
    assert job1.result()['created'] == 3
    assert set(d['_key'] for d in job2.result()) == {'1', '2', '3'}
    assert set(d['_key'] for d in job3.result()) == {'1'}


def test_batch_clear():
    assert len(col) == 0
    batch = db.batch(return_result=True)
    batch_col = batch.collection(col_name)
    job1 = batch_col.insert({'_key': '1', 'val': 1})
    job2 = batch_col.insert({'_key': '2', 'val': 2})
    batch.clear()
    batch.commit()

    assert len(col) == 0
    assert job1.status() == 'pending'
    assert job2.status() == 'pending'
