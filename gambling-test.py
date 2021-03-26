from flask import Flask, request, render_template, session, redirect
import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date

app = Flask(__name__)

def get_full_team_array(datelist, start_date, end_date):			#This function creates the full_team_array as well as seperates the current day teams/scores from the full list of teams
	rank_array = ['(1) ', '(2) ','(3) ', '(4) ', '(5) ' ,'(6) ', '(7) ', '(8) ', '(9) ', '(10) ', '(11) ', '(12) ', '(13) ', '(14) ', '(15) ', '(16) ', '(17) ', '(18) ', '(19) ', '(20) ', '(21) ', '(22) ', '(23) ', '(24) ', '(25) ']

	full_team_array = []
	current_day_team_array = []

	for x in range(start_date, end_date):
		date = datelist[x].strftime('%Y-%m-%d')
		url = 'https://www.thescore.com/ncaab/events/conference/Big%20Ten/date/' + date
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		teams = soup.find_all(attrs = {'class': 'EventCard__teamName--JweK5'})
		scores = soup.find_all(attrs = {'class' : 'EventCard__scoreColumn--2JZbq'})
		for team in teams:
			text = team.text
			if text not in rank_array:
				current_day_team_array.append(text)
				if text not in full_team_array:
					full_team_array.append(text)
					full_team_array.append(0)
					full_team_array.append(0)
					full_team_array.append(0)
					full_team_array.append(0)
					full_team_array.append(0)
					full_team_array.append(0)

		full_team_array = get_records(full_team_array, current_day_team_array, scores)
		current_day_team_array = []

	df = create_data_frame(full_team_array)
	return df



def	get_records(full_team_array, current_day_team_array, scores):			#This function turns the current day team array into games(H,A,Home Score, Away Score) and then also assings the correct records to teams.

	score_count = 0
	for i in range(1, len(current_day_team_array) * 2, 2):
		current_day_team_array.insert(i, scores[score_count].text)
		score_count += 1

	current_day_team_array = [current_day_team_array[x:x+4] for x in range(0, len(current_day_team_array), 4)]
	
	for i in range(0, len(current_day_team_array)):
		if(current_day_team_array[i][1] != ''):
			if int(current_day_team_array[i][1]) > int(current_day_team_array[i][3]):
				for j in range(0, len(full_team_array)):
					if full_team_array[j] == current_day_team_array[i][0]:
						full_team_array[j+1] += 1
						full_team_array[j+5] += 1
					if full_team_array[j] == current_day_team_array[i][2]:
						full_team_array[j+2] += 1
						full_team_array[j+4] += 1
			if int(current_day_team_array[i][1]) < int(current_day_team_array[i][3]):
				for j in range(0, len(full_team_array)):
					if full_team_array[j] == current_day_team_array[i][2]:
						full_team_array[j+1] += 1
						full_team_array[j+3] += 1
					if full_team_array[j] == current_day_team_array[i][0]:
						full_team_array[j+2] += 1
						full_team_array[j+6] += 1
	
	#full_team_array = [full_team_array[x:x+7] for x in range(0, len(full_team_array), 7)]
	return full_team_array


def create_data_frame(full_team_array):	 #Creating and printing the final pandas dataframe. Full_team_array is input and the dataframe currently includes wins,losses, H/A wins and losses.
	full_team_array = [full_team_array[x:x+7] for x in range(0, len(full_team_array), 7)]

	teams = []
	wins = []
	losses = []
	homewins = []
	homelosses = []
	awaywins = []
	awaylosses = []
	for i in range(0, len(full_team_array)):
		teams.append(full_team_array[i][0])
		wins.append(full_team_array[i][1])
		losses.append(full_team_array[i][2])
		homewins.append(full_team_array[i][3])
		homelosses.append(full_team_array[i][4])
		awaywins.append(full_team_array[i][5])
		awaylosses.append(full_team_array[i][6])
	
	df = pd.DataFrame(
		{
			'Team': teams,
			'Wins': wins,
			'Losses': losses,
			'Home Wins': homewins,
			'Home Losses': homelosses,
			'Away Wins' : awaywins,
			'Away Losses' : awaylosses
		})
	return df

datelist = pd.date_range(datetime.datetime(2020, 11, 25), periods = 60)
df = get_full_team_array(datelist, 0, 20)

@app.route('/')
def index():
    
    #df = pd.DataFrame({'A': [0, 1, 2, 3, 4],
    #                   'B': [5, 6, 7, 8, 9],
     #                  'C': ['a', 'b', 'c--', 'd', 'e']})
    #return df.to_html(header='true' , table_id='table')    
	return render_template('simple.html',  my_title='Test', my_content=df.columns.values)
    
	#return "<h1>Welcome to our server !!</h1>
#if __name__ == '__main__':
#    app.run(debug=True)
