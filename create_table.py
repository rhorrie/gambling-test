from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from testing_dicts import *
import datetime
from datetime import date
import time
import pickle

app = Flask(__name__)

<<<<<<< HEAD
datelist = pd.date_range(start="2021-05-20", end=(datetime.datetime.today() - datetime.timedelta(days=1)))
team_dict = get_full_team_array(datelist)
=======
#datelist = pd.date_range(start="2021-05-05", end=(datetime.datetime.today() - datetime.timedelta(days=1)))
#team_dict = get_full_team_array(datelist)
>>>>>>> 2c195d6cf677fa2ed4fb37624e964e7aeb9b6978

#file = open("data.pkl", "wb")
#pickle.dump(team_dict, file)
#file.close()

team_dict = pickle.load(open("data.pkl", "rb"))

df = pd.DataFrame.from_dict(team_dict)

@app.route('/')
def index():

	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
	app.run(debug=True)
<<<<<<< HEAD


#Taking too long to create table in heroku. Workers are timing out. Look at this link https://bigishdata.com/2016/12/15/running-python-background-jobs-with-heroku/
# to possibly gain a better understanding of having a worker.py do the webscraping in the background so there is no worry of timing out.
=======
>>>>>>> 2c195d6cf677fa2ed4fb37624e964e7aeb9b6978
