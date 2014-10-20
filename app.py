from flask import Flask, render_template, request
import sqlite3
import csv
app = Flask(__name__)

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
    
    c = conn.cursor()
    try:
        c.execute("CREATE TABLE post(title TEXT UNIQUE, content TEXT, date TEXT, author TEXT)")
        print "Creating new table called 'post' in blog.db"
    except:
        print "Adding to table 'post' in blog.db"

    BASE = "INSERT INTO post VALUES('%(title)s', '%(content)s', '%(date)s', '%(author)s')"
    for l in csv.DictReader(open(csvname)):
        try:
            q = BASE%l
            c.execute(q)
            print q

        except:
            pass
    conn.commit()

    return csv.DictReader(open(csvname))



if __name__=="__main__":
    app.debug=True
    app.run(port=5000)

