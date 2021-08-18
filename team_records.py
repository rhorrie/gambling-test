from flask import Flask, request, render_template, session, redirect
import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime
from datetime import date

def get_full_team_array(datelist, address):			#This function creates the full_team_array as well as seperates the current day teams/scores from the full list of teams
	
	#This is not used currently, but will be once NCAA basketball starts and possibly NCAA football as well. Most likely.
	rank_array = ['(1) ', '(2) ','(3) ', '(4) ', '(5) ' ,'(6) ', '(7) ', '(8) ', '(9) ', '(10) ', '(11) ', '(12) ', '(13) ', '(14) ', '(15) ', '(16) ', '(17) ', '(18) ', '(19) ', '(20) ', '(21) ', '(22) ', '(23) ', '(24) ', '(25) ']

	#Creating team dictionary to contain all teams and records until I can enter the info into database with SQLite3
	team_dict = {"Name":[], "Wins":[], "Losses":[], "Home Wins":[], "Home Losses":[], "Away Wins":[], "Away Losses":[]}
	current_day_team_array = []

	#Inserting team names into dictionary to use in the future. 
	for date in datelist:
		url = address + date
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		teams = soup.find_all(attrs = {'class': 'EventCard__teamName--JweK5'})
		scores = soup.find_all(attrs = {'class' : 'EventCard__scoreColumn--2JZbq'})
		finals = soup.find_all(attrs = {'class' : 'EventCard__clockColumn--3lEPz'})
		for team in teams:
			text = team.text
			if text not in rank_array:
				current_day_team_array.append(text)
				if text not in team_dict["Name"]:
					team_dict["Name"].append(text)
					team_dict["Wins"].append(0)
					team_dict["Losses"].append(0)
					team_dict["Home Wins"].append(0)
					team_dict["Home Losses"].append(0)
					team_dict["Away Wins"].append(0)
					team_dict["Away Losses"].append(0)

		
		#Calling get_records to determine the record information for every team.
		team_dict = get_records(team_dict, current_day_team_array, scores, finals)

		#Resets the current day array for the loop
		current_day_team_array = []

	return team_dict



def	get_records(team_dict, current_day_team_array, scores, finals):			#This function turns the current day team array into games(H,A,Home Score, Away Score) and then also assigns the correct records to teams.

	score_count = 0
	for i in range(1, len(current_day_team_array) * 2, 2):
		current_day_team_array.insert(i, scores[score_count].text)
		score_count += 1

	current_day_team_array = [current_day_team_array[x:x+4] for x in range(0, len(current_day_team_array), 4)]
	
	for i in range(0, len(current_day_team_array)):
		if(current_day_team_array[i][1] != '' and 'Postponed' not in finals[i].text):
			if int(current_day_team_array[i][1]) > int(current_day_team_array[i][3]):
				for j in range(0, len(team_dict["Name"])):
					if team_dict["Name"][j] == current_day_team_array[i][0]:
						team_dict["Wins"][j] += 1
						team_dict["Away Wins"][j] += 1
					if team_dict["Name"][j] == current_day_team_array[i][2]:
						team_dict["Losses"][j] += 1
						team_dict["Home Losses"][j] += 1
			if int(current_day_team_array[i][1]) < int(current_day_team_array[i][3]):
				for j in range(0, len(team_dict["Name"])):
					if team_dict["Name"][j] == current_day_team_array[i][2]:
						team_dict["Wins"][j] += 1
						team_dict["Home Wins"][j] += 1
					if team_dict["Name"][j] == current_day_team_array[i][0]:
						team_dict["Losses"][j] += 1
						team_dict["Away Losses"][j] += 1
	
	return team_dict

#See if I can use unpickle the .pkl file back to the dataframe and then append the new info
# and then repickle the file basically recusively (not really) just doing it everyday.
