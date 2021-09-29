#Update the nfl table every week on tuesdays. Work in progress still.

import datetime
from datetime import date
import time
import sqlite3
import psycopg2
from local_team_records import *

con = psycopg2.connect(database="localdb")
cur = con.cursor()

days = date(2021, 9, 28) - date(2021, 9, 7)
week = int(days.days/7)
nfl_datelist = ['2021-' + str(week)]
#nfl_datelist = ['2021-preseason_3'] #add 4 if works locally
daily_dict = get_full_team_array(nfl_datelist, 'https://www.thescore.com/nfl/events/date/')

for i in range(0, len(daily_dict["Name"])):	
	cur.execute("UPDATE nfl_gambling SET wins=wins+%s, losses=losses+%s, homewins=homewins+%s, homelosses=homelosses + %s, awaywins=awaywins+%s, awaylosses=awaylosses+%s WHERE Name = %s", (daily_dict["Wins"][i], daily_dict["Losses"][i], daily_dict["Home Wins"][i], daily_dict["Home Losses"][i], daily_dict["Away Wins"][i], daily_dict["Away Losses"][i], daily_dict["Name"][i]))
con.commit()