#Just a file to run test SQL code when needed.


#import sqlite3
#con = sqlite3.connect('test.db')
#con.execute('''CREATE TABLE gambling
#		(name text, wins int, losses int, homewins int, homelosses int, awaywins int, awaylosses int)''')
#con.commit()

#import sqlite3
#con = sqlite3.connect('test.db')
#con.execute('DROP TABLE gambling')
#con.commit()

import psycopg2

conn = psycopg2.connect(database="gambling")

cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS test
	(Name text, wins int);''')

conn.commit()

print(cur.execute('''SELECT * from test'''))