from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BlockingScheduler()

q = Queue(connection=conn)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=2)
def scheduled_job():
	q.enqueue(execfile('update_table_daily.py'))

sched.start()