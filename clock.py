
#This runs the update table function to update MLB tables.

from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from pytz import timezone

#Schedule update_table_daily to run mon-fri at I believe 2 AM. Could be a timezone issue though.

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=2)
def timed_job_test():
	execfile('nfl_weekly_table.py')
sched.start()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=2)
def mlb_scheduled_job():
	execfile('mlb_daily_table.py')
sched.start()

@sched.scheduled_job('cron', day_of_week='tue', hour=2)
def nfl_scheduled_job():
	execfile('nfl_weekly_table.py')
sched.start()


#Need to solve the timezone issue. Other than that everything is up and running and good to go. 
