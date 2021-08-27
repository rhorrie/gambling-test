from flask import Flask, request, render_template, session, redirect
import requests
import pandas as pd
import sqlite3
from local_team_records import * 
import psycopg2


#Connects to database and drops tables if they already exists, this is mainly just for testing purposes as it will not run more then once on heroku.
con = psycopg2.connect(database="localdb")
cur = con.cursor()

cur.execute('''DROP TABLE mlb_gambling''')
cur.execute('''DROP TABLE nfl_gambling''')

##Creates MLB gambling table if it does not already exist. Just a test right now
cur.execute('''CREATE TABLE IF NOT EXISTS mlb_gambling
		(name text UNIQUE, wins int, losses int, homewins int, homelosses int, awaywins int, awaylosses int, plusminus decimal)''')
#
##Creates NFL gamlbing table if it does not already exist. 
cur.execute('''CREATE TABLE IF NOT EXISTS nfl_gambling
		(name text UNIQUE, wins int, losses int, homewins int, homelosses int, awaywins int, awaylosses int, plusminus decimal)''')

#Commit the table creations
con.commit()

#Determines the dates you choose and returns the team info in dict format for mlb stats
mlb_datelist = pd.date_range(start="2021-08-01", end=(datetime.datetime.today() - datetime.timedelta(days=1)))
string_datelist = []
for x in mlb_datelist:
	date = x.strftime('%Y-%m-%d')
	string_datelist.append(date)
mlb_team_dict = get_full_team_array(string_datelist, 'https://www.thescore.com/mlb/events/date/')

#Determines the "dates" you want for NFL. These are a little different because they are just numbered weeks. Calls to get the team array for NFL stats
nfl_datelist = ['2021-preseason_2']
nfl_team_dict = get_full_team_array(nfl_datelist, 'https://www.thescore.com/nfl/events/date/')

#Inserts dict values into MLB gambling table 
for i in range(0, len(mlb_team_dict["Name"])):
	cur.execute("INSERT INTO mlb_gambling VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (mlb_team_dict['Name'][i], mlb_team_dict['Wins'][i], mlb_team_dict['Losses'][i], mlb_team_dict['Home Wins'][i], mlb_team_dict['Home Losses'][i], mlb_team_dict['Away Wins'][i], mlb_team_dict['Away Losses'][i], 0))

#Inserts dict values into NFL gambling table
for i in range(0, len(nfl_team_dict["Name"])):
	cur.execute("INSERT INTO nfl_gambling VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (nfl_team_dict['Name'][i], nfl_team_dict['Wins'][i], nfl_team_dict['Losses'][i], nfl_team_dict['Home Wins'][i], nfl_team_dict['Home Losses'][i], nfl_team_dict['Away Wins'][i], nfl_team_dict['Away Losses'][i], 0))

#Commits changes made to MLB and NFL gambling tables
con.commit()


#Code below is only used for local testing.
#Creates the flask application
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():

	#Connects to database in order to have a continued connection. Displays all info from the MLB gambling table.
	con = psycopg2.connect(database="localdb")
	df = pd.read_sql_query("SELECT * from mlb_gambling", con)
	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

@app.route('/nfl/')
def nfl():
	
	#Connects to database in order to have a continued connection. Displays all info from the NFL gambling table.
	con = psycopg2.connect(database="localdb")
	df = pd.read_sql_query("SELECT * from nfl_gambling", con)
	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
	app.run(debug=True)
