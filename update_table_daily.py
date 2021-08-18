#This is only implemented for MLB as of right now.



from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from testing_dicts import *
import datetime
from datetime import date
import time
import sqlite3

#Connection to database
con = sqlite3.connect('test.db')

#Getting yesterdays game outcomes
datelist = pd.date_range(start=datetime.datetime.today() - datetime.timedelta(days=1), end=datetime.datetime.today() - datetime.timedelta(days=1))
daily_dict = get_full_team_array(datelist)

#Updating table values to include todays game outcomes
for i in range(0, len(daily_dict["Name"])):	
	con.execute("UPDATE mlb_gambling SET wins=wins+?, losses=losses+?, homewins=homewins+?, homelosses=homelosses + ?, awaywins=awaywins+?, awaylosses=awaylosses+? WHERE Name = ?", (daily_dict["Wins"][i], daily_dict["Losses"][i], daily_dict["Home Wins"][i], daily_dict["Home Losses"][i], daily_dict["Away Wins"][i], daily_dict["Away Losses"][i], daily_dict["Name"][i]))
con.commit()
