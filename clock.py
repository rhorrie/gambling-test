from apscheduler.schedulers.blocking import BlockingScheduler
from rq import Queue
from worker import conn

#Schedule update_table_daily to run mon-fri at I believe 2 AM. Could be a timezone issue though.

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=2)

def scheduled_job():
	execfile('update_table_daily.py')

sched.start()
