from flask import Flask, request, render_template, session, redirect
import requests
import pandas as pd
import sqlite3
from team_records import * 
import psycopg2
import os

#Connects to database and drops tables if they already exists, this is mainly just for testing purposes as it will not run more then once on heroku.
DATABASE_URL = os.environ['DATABASE_URL']
con = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = con.cursor()

##Creates MLB gambling table if it does not already exist. Just a test right now
cur.execute('''CREATE TABLE IF NOT EXISTS mlb_gambling
		(name text UNIQUE, wins int, losses int, homewins int, homelosses int, awaywins int, awaylosses int, plusminus decimal)''')

##Creates NFL gamlbing table if it does not already exist. 
cur.execute('''CREATE TABLE IF NOT EXISTS nfl_gambling
		(name text UNIQUE, wins int, losses int, homewins int, homelosses int, awaywins int, awaylosses int, plusminus decimal)''')

##Commit the table creations
con.commit()

#Creates the flask application
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():

	#Connects to database in order to have a continued connection. Displays all info from the MLB gambling table.
	DATABASE_URL = os.environ['DATABASE_URL']
	con = psycopg2.connect(DATABASE_URL, sslmode='require')
	df = pd.read_sql_query("SELECT * from mlb_gambling", con)
	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

@app.route('/nfl/')
def nfl():
	
	#Connects to database in order to have a continued connection. Displays all info from the NFL gambling table.
	DATABASE_URL = os.environ['DATABASE_URL']
	con = psycopg2.connect(DATABASE_URL, sslmode='require')
	df = pd.read_sql_query("SELECT * from nfl_gambling", con)
	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
	app.run(debug=True)

#/Users/Horrie13/Library/Application Support/Postgres/var-13


#Creates table "Gambling" and also creates webpage which hosts the table.
#This only needs to be ran one time and it automatically updates the table
#whenever the table is edited. This needs to be the web dyno in heroku.

#No longer using create_table.py to originally create the table. All I need to do now is figure out how to have background workers
# in Heroku to perform the webscraping and updates on the table and we should be set.