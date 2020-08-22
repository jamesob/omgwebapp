import sys
import signal
import datetime
import time

import logging

from . import db

logging.basicConfig()
log = logging.getLogger(__name__)


def _signal_handler(signal, frame, *args, **kwargs):
    if not db.database.is_closed():
        db.database.close()
    print(f'caught signal {signal} - exiting', file=sys.stderr)
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    db.create_tables()
    db.database.connect()
    print(f"worker up, connected to {db.database.database}")

    while True:
        nextjob = db.claim_next_job()

        if nextjob:
            print(f"got job! {nextjob}")
            params = nextjob.params

            if nextjob.job_type == 'greet':
                print(f"Hey {params['name']}, {params['msg']}")
            elif nextjob.job_type == 'yell':
                print(f"{params['msg'].upper()}!!!")

            nextjob.completed_at = datetime.datetime.now()
            nextjob.save()
            print(f'completed job {nextjob}')

        time.sleep(0.2)
