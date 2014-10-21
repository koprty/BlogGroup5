from flask import Flask, render_template, request
import sqlite3
import csv
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
def index():
    initialize()
    if request.method == "GET":
        return render_template("index.html",posts=getPosts())
    else:
        pass

@app.route("/post/<title>")
def post(title=None):
    return render_template("post.html",title=title)



def initialize():
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


def getPosts():
    csvname = "data.csv"
    return csv.DictReader(open(csvname))

def getComments():
    csvname = "comments.csv"
    return csv.DictReader(open(csvname))

if __name__=="__main__":
    app.debug=True
    app.run(port=5000)

