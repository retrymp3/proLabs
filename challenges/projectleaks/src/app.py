from flask import Flask,render_template,request,session,redirect,make_response
import os
import subprocess
import sqlite3
import uuid

curr_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

def get_db_connection():
    conn = sqlite3.connect('chall.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/',methods=["GET"])
def index():
    if(not session.get('user')):
       return redirect("/login")
    res = make_response(render_template("index.html",user_name=session.get('user')))
    res.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self';"
    return res

@app.route('/login',methods=["POST","GET"])
def login():
    if(session.get('user')):
       return redirect("/")
    if(request.method=="GET"):
        return render_template("login.html")
    try:
        user = request.form['user'].strip()
        passw = request.form['pass'].strip()
        if(user=="admin" and passw=="f50102afcb3a42518cbb1eaac1cbaa52"):
            session['admin'] = True
            session['user'] = user
        elif(user=="admin" and passw != "f50102afcb3a42518cbb1eaac1cbaa52"):
            return render_template("login.html",message="Incorrect password")
        else:
            session['user'] = user
    except Exception as e:
        return render_template("error.html",error=e)
    return redirect("/")

@app.route('/note',methods=["POST","GET"])
def note():
    if(not session.get('user')):
       return redirect("/login")
    if(request.method=="GET"):
        conn = get_db_connection()
        cur = conn.cursor()
        notes = cur.execute('SELECT note FROM notes where user=?',(session.get('user'),)).fetchall()
        conn.close()
        if(not notes):
            return ""
        return f"""
        <html>
        <head>
        <title>Notes</title>
        <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self';">
        </head>
        <body>
        {notes[0]['note']}
        </body>
        </html>
        """
    note = request.form['note']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (note, user) VALUES (?, ?)",(note, session.get('user'),))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route('/search',methods=["GET"])
def search():
    if(not session.get('user')):
       return redirect("/login")
    search = request.args.get('search')
    conn = get_db_connection()
    cur = conn.cursor()
    notes = cur.execute("SELECT note FROM notes where note like ? and user=? ",(search+'%',session.get('user'),)).fetchone()
    conn.close()
    if(not notes):
        return "No results found"
    return "<iframe srcdoc="+notes['note']+" sandbox></iframe>"

@app.route('/visit',methods=["GET"])
def visit():
    url = request.args.get('url').strip()
    subprocess.Popen(["python3",curr_dir+"/bot/bot.py",url])
    return "Reported"

if(__name__=="__main__"):
    app.run(host="0.0.0.0",port=5000,debug=True)