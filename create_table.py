from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from gambling_info import *
import datetime
from datetime import date

app = Flask(__name__)

datelist = pd.date_range(start="2021-05-05", end=(datetime.datetime.today() - datetime.timedelta(days=1)))
get_full_team_array(datelist)

df = pd.read_pickle("./test.pkl")	


@app.route('/')
def index():
	#return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
	return render_template('new_test.html', column_names=df.columns.values, row_data=list(df.values.tolist()), zip=zip)

if __name__ == '__main__':
	app.run(debug=True)