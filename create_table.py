from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from testing_dicts import *
import datetime
from datetime import date
import time
import pickle

app = Flask(__name__)

datelist = pd.date_range(start="2021-05-05", end=(datetime.datetime.today() - datetime.timedelta(days=1)))
team_dict = get_full_team_array(datelist)

file = open("data.pkl", "wb")
pickle.dump(team_dict, file)
file.close()

df = pd.DataFrame.from_dict(team_dict)

@app.route('/')
def index():

	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
	app.run(debug=True)
