
#This runs the update table function to update MLB tables.

from apscheduler.schedulers.blocking import BlockingScheduler

#Schedule update_table_daily to run mon-fri at I believe 2 AM. Could be a timezone issue though.

sched = BlockingScheduler()

@sched.mlb_scheduled_job('cron', day_of_week='mon-fri', hour=2)
def mlb_scheduled_job():
	execfile('mlb_daily_table.py')

@sched.nfl_scheduled_job('cron', dary_of_week='tue', hour=2)
def nfl_scheduled_job():
	execfile('nfl_weekly_table.py')


sched.start()
