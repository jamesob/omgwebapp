import pytest
from playhouse.sqlite_ext import SqliteExtDatabase

from . import db


@pytest.fixture
def memdb():
    mdb = SqliteExtDatabase(':memory:')
    models = [db.Job]
    mdb.bind(models)
    mdb.connect()
    mdb.create_tables(models)

    yield mdb

    mdb.close()
