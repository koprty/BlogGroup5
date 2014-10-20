import sqlite3
import csv
#from flask import Flask, render_template

'''
Bugs to keep in mind:
1) <"> and <'> and <,> will cause problems- the first two in entry to the database, while the last one may cause a misread in the csv file
'''

conn = sqlite3.connect('blog.db')
csvname = "data.csv"

c = conn.cursor()
try:
    c.execute("CREATE TABLE post(name TEXT UNIQUE, content TEXT, date TEXT, author TEXT)")
    print "Creating new table called 'post' in blog.db"
except:
    print "Adding to table 'post' in blog.db"

BASE = "INSERT INTO post VALUES('%(name)s', '%(content)s', '%(date)s', '%(author)s')"
for l in csv.DictReader(open(csvname)):
    try:
        q = BASE%l
        c.execute(q)
        print q

    except:
        pass
conn.commit()


def addBlog(s):
    f.open(csvname,'w+')
    f.write(s)
    f.close


'''
1. python this file
2. run sqlite3 blog.db
example sqlite commands:
select * from post;
select content from post where name == "Welcome";

If you python twice-> there will not be a repeat of the elements
this seems to be also true when there is a repeat of the same element in the table
'''

