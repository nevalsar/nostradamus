from __future__ import print_function
import MySQLdb as mdb
from os import system
import os


# db = mdb.connect('10.5.18.67','12CS30026','dual12','12CS30026')
db = mdb.connect('localhost','root','pass','fun')
cursor = db.cursor()


def executer(query):
	print(query)
	cursor.execute(query)

def fetcher():
	return cursor.fetchall()



def main():
	try:
		os.remove('reviews')
	except:
		pass
	try:
		os.remove('scores')
	except:
		pass
	executer("select rid, text from Review where sentiment_score is NULL")
	results = fetcher()
	with open("reviews","a") as f:
		for result in results:
			f.write(str(result[0])+"====>>>>"+str(result[1])+'\n')
	system("torify python sentiment.py")

	with open("scores") as f:
		lines = f.readlines()
	for line in lines:
		line = line.strip()
		line = line.split(" ")
		executer("update Review set sentiment_score = {0} where rid = {1}".format(line[1],line[0]))
	try:
		os.remove('reviews')
	except:
		pass
	try:
		os.remove('scores')
	except:
		pass	
	db.commit()

main()