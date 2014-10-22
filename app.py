from flask import Flask, render_template, request
import sqlite3
import csv
app = Flask(__name__)

conn = sqlite3.connect('blog.db')
csvname = "data.csv"
comcsvname = "comments.csv"
c = conn.cursor()

@app.route("/",methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
def index():
    if request.method == "GET":
        return render_template("index.html",posts=getPosts())
    else:
        pass

@app.route("/post/<title>/<id>")
def post(title = None,id=None):
    curr_post={}
    for x in getPosts():
        if x['id'] == id:
            curr_post=x
    curr_comments = [y for y in getComments() if y['id']==id]
    print curr_comments
    return render_template("post.html",post=curr_post,comments=curr_comments)

def initialize():
    try:
        c.execute("CREATE TABLE post(id INTEGER UNIQUE, title TEXT UNIQUE, content TEXT, date TEXT, author TEXT)")
        c.execute("CREATE TABLE comments(id INTEGER UNIQUE, content TEXT, date TEXT, author TEXT)")
        print "Creating new tables called 'post' and 'comments' in blog.db"
    except:
        print "Adding to tables 'post' and 'comments' in blog.db"
    BASE = "INSERT INTO post VALUES('%(id)s','%(title)s', '%(content)s', '%(date)s', '%(author)s')"
    for l in csv.DictReader(open(csvname)):
        try:
            q = BASE%l
            c.execute(q)
        except:
            pass
    conn.commit()
    BASE = "INSERT INTO comments VALUES('%(id)s','%(content)s', '%(date)s', '%(author)s')"
    for l in csv.DictReader(open(comcsvname)):
        try:
            q = BASE%l
            c.execute(q)
        except:
            pass
    conn.commit()

initialize()

def getPosts():
    return csv.DictReader(open(csvname))

def getComments():
    return csv.DictReader(open(comcsvname))

if __name__=="__main__":
    app.debug=True
    app.run(port=5000)

