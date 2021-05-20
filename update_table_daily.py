from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from testing_dicts import *
import datetime
from datetime import date
import time
import pickle

app = Flask(__name__)

datelist = pd.date_range(start=datetime.datetime.today() - datetime.timedelta(days=1), end=datetime.datetime.today() - datetime.timedelta(days=1))
daily_dict = get_full_team_array(datelist)

total_dict = pickle.load(open("data.pkl", "rb"))

for i in range(0, len(total_dict["Name"])):
	for j in range(0, len(daily_dict["Name"])):
		if total_dict["Name"][i] == daily_dict["Name"][j]:
			total_dict["Wins"][i] += daily_dict["Wins"][j]
			total_dict["Losses"][i] += daily_dict["Losses"][j]
			total_dict["Home Wins"][i] += daily_dict["Home Wins"][j]
			total_dict["Home Losses"][i] += daily_dict["Home Losses"][j]
			total_dict["Away Wins"][i] += daily_dict["Away Wins"][j]
			total_dict["Away Losses"][i] += daily_dict["Away Losses"][j]

df = pd.DataFrame.from_dict(total_dict)

@app.route('/')
def index():
	
	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
	app.run(debug=True)