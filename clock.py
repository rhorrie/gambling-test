
#This runs the update table function to update MLB tables.

from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from pytz import timezone
from nfl_weekly_table import nfl_weekly
from mlb_daily_table import mlb_daily
from plusminus import find_plusminus

#Schedule update_table_daily to run mon-fri at I believe 2 AM. Could be a timezone issue though.

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=2)
def mlb_scheduled_job():
	mlb_daily()
	find_plusminus()
sched.start()

@sched.scheduled_job('cron', day_of_week='tue', hour=2)
def nfl_scheduled_job():
	nfl_weekly()
	find_plusminus()
sched.start()


#Need to solve the timezone issue. Other than that everything is up and running and good to go. 
