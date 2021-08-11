from flask import Flask, request, render_template, session, redirect
import requests
import pandas as pd
import sqlite3
from testing_dicts import * 

#Drops table if it already exists
con = sqlite3.connect('test.db')
con.execute('DROP TABLE gambling')
con.commit()

#Recreates the table, just a test right now
con.execute('''CREATE TABLE IF NOT EXISTS gambling
		(name text UNIQUE, wins int, losses int, homewins int, homelosses int, awaywins int, awaylosses int)''')
con.commit()

#Determines the dates you choose and returns the team info in dict format
datelist = pd.date_range(start="2021-08-01", end=(datetime.datetime.today() - datetime.timedelta(days=1)))
team_dict = get_full_team_array(datelist)

#Inserts dict values into gambling table 
for i in range(0, len(team_dict["Name"])):
	con.execute("INSERT INTO gambling VALUES(?, ?, ?, ?, ?, ?, ?)", (team_dict['Name'][i], team_dict['Wins'][i], team_dict['Losses'][i], team_dict['Home Wins'][i], team_dict['Home Losses'][i], team_dict['Away Wins'][i], team_dict['Away Losses'][i]))
con.commit()

#Creates the flask application
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():

	#Connects to database in order to have a continued connection. Displays all info form gambling table.
	con = sqlite3.connect('test.db')
	df = pd.read_sql_query("SELECT * from gambling", con)
	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
	app.run(debug=True)


#Creates table "Gambling" and also creates webpaeg which hosts the table.
#This only needs to be ran one time and it automatically updates the table
#whenever the table is edited. This needs to be the web dyno in heroku.

#No longer using create_table.py to originally create the table. All I need to do now is figure out how to have background workers
# in Heroku to perform the webscraping and updates on the table and we should be set.