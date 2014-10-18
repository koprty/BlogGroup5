import sqlite3
import csv
#from flask import Flask, render_template


conn = sqlite3.connect('blog.db')

csvname = "data.csv"

c = conn.cursor()
try:
    c.execute("CREATE TABLE post(name TEXT UNIQUE, content TEXT UNIQUE, date TEXT, author TEXT)")
    print "Creating new table for db"

except:
    print "Adding to created table"

BASE = "INSERT INTO post VALUES('%(name)s', '%(content)s', '%(date)s', '%(author)s')"
for l in csv.DictReader(open(csvname)):
    q = BASE%l
    print q
    c.execute(q)

conn.commit()
