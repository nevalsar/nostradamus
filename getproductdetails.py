#!usr/bin/python

import MySQLdb as mdb
db = mdb.connect('10.5.18.67','12CS30026','dual12','12CS30026')
cursor = db.cursor()

pid = raw_input()
