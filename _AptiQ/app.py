from flask import Flask,flash,request,redirect,render_template,url_for,session
import sqlite3
import os
from random import randint

app=Flask(__name__)
app.secret_key="k3jnk5bHb4BiLJnI7cYxbl"

def get_connection():
    f=os.path.isfile("questions.db")
    con=sqlite3.connect("questions.db")
    if not f:
        cur=con.cursor()
        with open("schema.sql","r") as file:
            cur.executescript(file.read())
        con.commit()
    return con

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/")
def index():
    session["f"]=1
    return render_template("index.html")

@app.route("/easy")
def easy():
    if "f" in session.keys():
        session.pop("f",None)
        con=get_connection()
        cur=con.cursor()
        s=set()
        while len(s)<10:
            s.add((randint(1,43),))
        
        l=[]
        for i in s:
            cur.execute("select * from Questions where id=?",i)
            l.append(cur.fetchone())
        session["l"]=l
        return render_template("easy.html",l=l)
    return redirect(url_for("index"))

@app.route("/medium")
def medium():
    if "f" in session.keys():
        session.pop("f",None)
        con=get_connection()
        cur=con.cursor()
        s=set()
        while len(s)<15:
            s.add((randint(1,43),))
        
        l=[]
        for i in s:
            cur.execute("select * from Questions where id=?",i)
            l.append(cur.fetchone())
        session["l"]=l
        return render_template("medium.html",l=l)
    return redirect(url_for("index"))

@app.route("/hard")
def hard():
    if "f" in session.keys():
        session.pop("f",None)
        con=get_connection()
        cur=con.cursor()
        s=set()
        while len(s)<20:
            s.add((randint(1,43),))
        
        l=[]
        for i in s:
            cur.execute("select * from Questions where id=?",i)
            l.append(cur.fetchone())
        session["l"]=l
        return render_template("hard.html",l=l)
    return redirect(url_for("index"))

@app.route("/result",methods=["GET","POST"])
def result():
    if request.method=="POST":
        c=0
        l=session["l"]
        session.pop("l",None)
        n=len(l)
        for i in range(n):
            if int(l[i][6])==int(request.form.get("q"+str(i),4)):
                c+=1
        return render_template("result.html",score=c,total=n)
    return redirect(url_for("index"))


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")
    
