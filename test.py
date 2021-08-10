import sqlite3
con = sqlite3.connect('test.db')
con.execute('''INSERT INTO gambling
		(name, wins, losses, homewins, homelosses, awaywins, awaylosses)
		VALUES(1,2,3,4,5,6,7)''')

con.commit()



#This file can be used to insert updated info into the dataframe that is already in use. Just find where the info needs to be inserted
# and insert it using sqlite3 as shown above. Can also be used for testing.


