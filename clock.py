from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

<<<<<<< HEAD
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=2)
=======
@sched.scheduled_job('cron', day_of_week='mon-sat', hour=2)
>>>>>>> 2c195d6cf677fa2ed4fb37624e964e7aeb9b6978
def scheduled_job():
	execfile('update_table_daily.py')

sched.start()
