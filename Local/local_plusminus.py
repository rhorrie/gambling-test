#Determines the plus/minus value just based off of a very simple weighted function I created and inserts the values into table.

import psycopg2

#Connecting to database and creating iterators to iterate over information from tables
con = psycopg2.connect(database="localdb")
mlb_iterator = con.cursor()
nfl_iterator = con.cursor() 
cur = con.cursor()

#Creating arrays for mlb and nfl information
mlb_team_array = []
nfl_team_array = []
mlb_plusminus_array = []
nfl_plusminus_array = []

#Updating mlb plus/minus column
mlb_iterator.execute('SELECT * FROM mlb_gambling')
for row in mlb_iterator:
	mlb_team_array.append(row[0])
	plusminus = (((row[1] * .4) + (row[3] * .2) + (row[5] * .6)) - ((row[2] * .4) + (row[4] * .6) + (row[6] * .2)))
	plusminus = round(plusminus, 2)
	mlb_plusminus_array.append(plusminus)
for i in range(0, len(mlb_team_array)):
	cur.execute('UPDATE mlb_gambling SET plusminus = %s WHERE name = %s', ((mlb_plusminus_array[i]), mlb_team_array[i]))

#Updating nfl plus/minsu column
nfl_iterator.execute('SELECT * FROM nfl_gambling')
for row in nfl_iterator:
	nfl_team_array.append(row[0])
	plusminus = (((row[1] * .4) + (row[3] * .2) + (row[5] * .6)) - ((row[2] * .4) + (row[4] * .6) + (row[6] * .2)))
	plusminus = round(plusminus, 2)
	nfl_plusminus_array.append(plusminus)
for i in range(0, len(nfl_team_array)):
	cur.execute('UPDATE nfl_gambling SET plusminus = %s WHERE name = %s', ((nfl_plusminus_array[i]), nfl_team_array[i]))

con.commit()


#This file can be used to insert updated info into the dataframe that is already in use. Just find where the info needs to be inserted
# and insert it using sqlite3 as shown above. Can also be used for testing.


