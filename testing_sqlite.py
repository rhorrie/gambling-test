import sqlite3
con = sqlite3.connect('test.db')
con.execute('''CREATE TABLE gambling
		(name text, wins int, losses int, homewins int, homelosses int, awaywins int, awaylosses int)''')
con.commit()
