#This is not implemented yet


from flask import Flask, request, render_template, session, redirect
import pandas as pd
import requests
from testing_dicts import *
from bs4 import BeautifulSoup
import datetime
from datetime import date
import time

def get_todays_matchups():
	todays_matchups = {'Away Team': [], 'Home Team': [], 'Lines': []}
	
	url = 'https://www.thescore.com/mlb/events/date/' + str(date.today())
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	teams = soup.select('div.EventCard__teamName--JweK5')
	lines = soup.select('div.EventCard__pregameScoreText--ow7eN')


	for i in range(0, len(teams)):	#Possibly make todays_matchups only have lines instead of both line and OU could make it easier
		away_text = matchups[i].text
		#home_text = teams[i+1].text
		todays_matchups["Away Team"].append(away_text)
		#todays_matchups["Home Team"].append(home_text)
	


	print(todays_matchups)






get_todays_matchups()

