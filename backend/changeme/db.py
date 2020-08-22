import datetime
import typing as t
import logging

import peewee as pw
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict
from playhouse.sqlite_ext import JSONField

from . import config

log = logging.getLogger(__name__)

database = connect(config.DB_URL)


class BaseModel(pw.Model):
    class Meta:
        database = database

    def asdict(self):
        return model_to_dict(self)


class Job(BaseModel):
    """A job submitted for execution by a user."""
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    started_at = pw.DateTimeField(null=True)
    completed_at = pw.DateTimeField(null=True)
    user = pw.CharField()
    job_type = pw.CharField(choices=(('greet',) * 2, ('yell',) * 2))
    params = JSONField()


def create_tables():
    with database:
        database.create_tables([Job])


# For more information on migrations, see
#
#   http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#migrate
#
# def mig_001():
#     from playhouse.migrate import SqliteMigrator, migrate
#     migrator = SqliteMigrator(database)
#     migrate(
#         migrator.add_column(Host._meta.table.__name__, 'python', Host.python),
#     )


def create_dev_data():
    if not config.DEV:
        log.warning("should not be calling this from non-dev environment")
        return
    ...


def claim_next_job() -> t.Optional[Job]:
    """Return the next Job to be started (presumably by the worker)."""
    ret = None

    with database.transaction() as txn:
        next_job = (
            Job.select()
            .where(Job.started_at.is_null(), Job.completed_at.is_null())
            .order_by(Job.created_at.asc())
            .first()
        )

        if not next_job:
            return None

        next_job.started_at = datetime.datetime.now()
        try:
            next_job.save()
        except pw.PeeweeException:
            log.exception('write-write conflict, rolling back')
            txn.rollback()
        else:
            ret = next_job

    return ret


def _pytest_claim_next_job(memdb):
    Job.create(
        started_at=datetime.datetime.now(),
        hosts=['localhost'],
        branches=['master', 'foo'],
        user='james',
        job_type='greet',
        params={'name': 'james', 'msg': 'how are you?'},
    )

    assert claim_next_job() is None

    j = Job.create(
        hosts=['localhost'],
        branches=['master', 'foo'],
        user='james',
        job_type='greet',
        params={'name': 'luke', 'msg': 'doing okay?'},
    )
    print(model_to_dict(j))

    assert claim_next_job().id == j.id

    j2 = Job.create(
        hosts=['localhost'],
        branches=['master', 'foo'],
        user='james',
        job_type='yell',
        params={'message': 'AAAAARGH!'},
    )

    assert claim_next_job().id == j2.id

    assert claim_next_job() is None
