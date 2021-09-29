#Update the nfl table every week on tuesdays. Work in progress still.

from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from team_records import *
import datetime
from datetime import date
import time
import sqlite3
import psycopg2

def nfl_weekly():
	DATABASE_URL = os.environ['DATABASE_URL']
	con = psycopg2.connect(DATABASE_URL, sslmode='require')
	cur = con.cursor()

	nfl_datelist = ['2021-preseason_3'] #add 4 if works locally
	daily_dict = get_full_team_array(nfl_datelist, 'https://www.thescore.com/nfl/events/date/')

	for i in range(0, len(daily_dict["Name"])):	
		cur.execute("UPDATE nfl_gambling SET wins=wins+%s, losses=losses+%s, homewins=homewins+%s, homelosses=homelosses + %s, awaywins=awaywins+%s, awaylosses=awaylosses+%s WHERE Name = %s", (daily_dict["Wins"][i], daily_dict["Losses"][i], daily_dict["Home Wins"][i], daily_dict["Home Losses"][i], daily_dict["Away Wins"][i], daily_dict["Away Losses"][i], daily_dict["Name"][i]))
	con.commit()