#Update the nfl table every week on tuesdays. Work in progress still.

import datetime
from datetime import date
import time
import sqlite3
import psycopg2
from team_records import *
import os

def nfl_weekly():
	#Connection to database
	DATABASE_URL = os.environ['DATABASE_URL']
	con = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = con.cursor()

	#Getting last weeks game outcomes
	days = datetime.date.today() - date(2021, 9, 7)
	week = int(days.days/7)
	nfl_datelist = ['2021-' + str(week)] 
	daily_dict = get_full_team_array(nfl_datelist, 'https://www.thescore.com/nfl/events/date/')

	#Updating table values to include last weeks game outcomes
	for i in range(0, len(daily_dict["Name"])):	
		cur.execute("UPDATE nfl_gambling SET wins=wins+%s, losses=losses+%s, homewins=homewins+%s, homelosses=homelosses + %s, awaywins=awaywins+%s, awaylosses=awaylosses+%s WHERE Name = %s", (daily_dict["Wins"][i], daily_dict["Losses"][i], daily_dict["Home Wins"][i], daily_dict["Home Losses"][i], daily_dict["Away Wins"][i], daily_dict["Away Losses"][i], daily_dict["Name"][i]))
	con.commit()