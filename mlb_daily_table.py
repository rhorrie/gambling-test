#This is only implemented for MLB as of right now.

import datetime
from datetime import date
import time
import sqlite3
import psycopg2
import os
from team_records import *

def mlb_daily():
	#Connection to database
	DATABASE_URL = os.environ['DATABASE_URL']
	con = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = con.cursor()
	
	#Getting yesterdays game outcomes
	datelist = pd.date_range(start=datetime.datetime.today() - datetime.timedelta(days=1), end=datetime.datetime.today() - datetime.timedelta(days=1))
	string_datelist = []
	for x in datelist:
		date = x.strftime('%Y-%m-%d')
		string_datelist.append(date)
	daily_dict = get_full_team_array(string_datelist, 'https://www.thescore.com/mlb/events/date/')
	
	#Updating table values to include todays game outcomes
	for i in range(0, len(daily_dict["Name"])):	
		cur.execute("UPDATE mlb_gambling SET wins=wins+%s, losses=losses+%s, homewins=homewins+%s, homelosses=homelosses + %s, awaywins=awaywins+%s, awaylosses=awaylosses+%s WHERE Name = %s", (daily_dict["Wins"][i], daily_dict["Losses"][i], daily_dict["Home Wins"][i], daily_dict["Home Losses"][i], daily_dict["Away Wins"][i], daily_dict["Away Losses"][i], daily_dict["Name"][i]))
	con.commit()
