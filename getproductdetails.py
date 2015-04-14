#!usr/bin/python

import MySQLdb as mdb
db = mdb.connect('10.5.18.67','12CS30026','dual12','12CS30026')
cursor = db.cursor()

pid = raw_input()
output = {}
reviews = []

sql = "SELECT * FROM Product WHERE pid = '" + pid + "'"
cursor.execute(sql)
if cursor.rowcount:
    row = cursor.fetchone()
    name = row[1]
    link = row[2]
    rating = row[3]
    category = row[5]

sql = "SELECT * FROM Review WHERE pid = '" + pid + "'"
cursor.execute(sql)
rc = cursor.rowcount

for i in range(0, rc):
	row = cursor.fetchone()
	title = row[2]
	text = row[3]
	nick = row[4]
	date = row[5]
	sentiment_score = row[6]
	reviews.append({'title': title, 'text': text, 'nick': nick, 'date': date, 'sentiment_score': sentiment_score})

output = {'name': name, 'link': link, 'rating': rating, 'category': category, 'reviews': reviews}
print output