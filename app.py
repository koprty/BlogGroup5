from flask import Flask, render_template, request, g
from time import localtime, strftime
import sqlite3
import csv

app = Flask(__name__)
DATABASE = 'blog.db'
csvname = "data.csv"
comcsvname = "comments.csv"

#return dictionary from db
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
        db.row_factory = dict_factory
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",posts=getPosts())

@app.route("/post/<id>/<title>",methods=['POST','GET'])
def post(title=None,id=None):
    if request.method == 'GET':
        curr_post = getPost(id)
        curr_comments = getComments(id)
        print curr_comments
        return render_template("post.html",post=curr_post,comments=curr_comments)
    else:
        curr_post = getPost(id)
        curr_comments = getComments(id)
        addComment()
        return render_template("post.html",post=curr_post,comments=curr_comments)

@app.route("/newpost", methods=["GET","POST"])
def newpost():
    return render_template("newPost.html");

def initialize():
    print "Initializing"
    conn = sqlite3.connect('blog.db')
    conn.row_factory = dict_factory
    
    c = conn.cursor()

    try:
        c.execute("CREATE TABLE posts(id INTEGER UNIQUE, title TEXT UNIQUE, content TEXT, date TEXT, author TEXT)")
        c.execute("CREATE TABLE comments(id INTEGER, content TEXT, date TEXT, author TEXT)")
        print "Creating new tables called 'posts' and 'comments' in blog.db"
    except:
        print "Adding to tables 'posts' and 'comments' in blog.db"
    BASE = "INSERT INTO posts VALUES('%(id)s','%(title)s', '%(content)s', '%(date)s', '%(author)s')"
    for l in csv.DictReader(open(csvname)):
        try:
            q = BASE%l
            c.execute(q)
            print "Inserted into db"
        except:
            pass
    conn.commit()
    BASE = "INSERT INTO comments VALUES('%(id)s','%(content)s', '%(date)s', '%(author)s')"
    c.execute("SELECT COUNT(*) FROM comments")
    count = c.fetchone()
    if(count["COUNT(*)"] == 0):
        for l in csv.DictReader(open(comcsvname)):
            try:
                q = BASE%l
                c.execute(q)
            except:
                print "Not inserted."
                pass
        conn.commit()

def addComment():
    time = strftime("%b %d %Y %I:%M %p",localtime())
    id = request.path.split("/")[2]
    c = get_db().cursor()
    #c.execute("SELECT COUNT(*) FROM comments")
    count = c.fetchone()
    name = request.form['name']
    comment = request.form['comment-text']
    v = (id,comment,time,name)
    c.execute("INSERT INTO comments VALUES (?,?,?,?)",v)
    #print name
    #print comment
    get_db().commit()
    print "Added comment"

def getPosts():
    c = get_db().cursor()
    c.execute("SELECT * FROM posts")
    posts = c.fetchall()
    return posts

def getPost(id):
    c = get_db().cursor()
    i = (id,)
    c.execute("SELECT * FROM posts where id=?",i)
    return c.fetchone()

def getComments(id):
    c = get_db().cursor()
    i = (id,)
    c.execute("SELECT * FROM comments WHERE id=?",i)
    comments = c.fetchall()
    print comments
    return comments

if __name__=="__main__":
    initialize()
    #conn = sqlite3.connect('blog.db')
    #getPosts()
    app.debug=True
    app.run(port=5000)

