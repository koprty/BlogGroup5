from flask import Flask, render_template, request
import sqlite3
import csv
app = Flask(__name__)

'''
Bugs to keep in mind:
1) <"> and <'> and <,> will cause problems- the first two in entry to the database, while the last one may cause a misread in the csv file
'''
@app.route("/",methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])

def index():
    if request.method == "GET":
        return render_template("index.html",posts=db())
    else:
        pass
@app.route("/title")
def title():
    pass



def db():
    conn = sqlite3.connect('blog.db')    
    csvname = "data.csv"
    comcsvname = "comments.csv"    
    c = conn.cursor()
    try:
        c.execute("CREATE TABLE post(title TEXT UNIQUE, content TEXT, date TEXT, author TEXT)")
        c.execute("CREATE TABLE comments(content TEXT, date TEXT, author TEXT)")
        print "Creating new tables called 'post' and 'comments' in blog.db"
    except:
        print "Adding to table 'post' in blog.db"
    BASE = "INSERT INTO post VALUES('%(title)s', '%(content)s', '%(date)s', '%(author)s')"
    for l in csv.DictReader(open(csvname)):
        try:
            q = BASE%l
            c.execute(q)
        except:
            pass
    conn.commit()
    
    BASE = "INSERT INTO comments VALUES('%(content)s', '%(date)s', '%(author)s')"
    for l in csv.DictReader(open(comcsvname)):
        try:
            q = BASE%l
            c.execute(q)
        except:
            pass
    conn.commit()
    return csv.DictReader(open(csvname))



if __name__=="__main__":
    app.debug=True
    app.run(port=5000)

def addBlog(s):
    f.open(csvname,'w+')
    f.write(s)
    f.close()

@app.route("tester", methods = ["GET", "POST"])
def bloggit():
    button = request.form["makePost"]
    if button = "submit":
        
        return render_template("index.html");
    
'''
1. python this file
2. run sqlite3 blog.db
example sqlite commands:
select * from post;
select content from post where name == "Welcome";

If you python twice-> there will not be a repeat of the elements
this seems to be also true when there is a repeat of the same element in the table
'''

