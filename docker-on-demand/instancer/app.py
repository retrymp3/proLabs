from flask import Flask, request, jsonify, redirect, session, url_for
from flask.templating import render_template
#from flask_wtf import RecaptchaField
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from database import db, Users, Challenges, SolvedChallenges, Deployment
import logging, uuid
import requests
import yaml
import hashlib
import json
import random
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

basedir = os.path.abspath(os.path.dirname(__file__))
pub_key = "6Lf5zu8kAAAAAMSBD2zCgLwVZyZiHDKavHrJkIcT"
app.secret_key = str(uuid.uuid4())
# logging.basicConfig(filename='debug.log', level=logging.WARNING,
                    # format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


CONFIG_PATH = "./config.yaml"
config = ""
with open(CONFIG_PATH, "r") as stream: # load config
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


CHALL_NAMES = config["images"]
API_URL = "http://localhost:5000"
print(CHALL_NAMES)

def PoW():
    x = os.urandom(16)
    target = hashlib.md5(x).hexdigest()
    out = f"MD5(X = {x[:13].hex()}+{'?'*6}) = " + target
    return x,target,out

# my code
@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/challenges")
def challenges():
    return render_template("challenges.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

# @app.route("/scoreboard")
# def scoreboard():
#     return render_template("scoreboard.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/flags")
def flags():
    return render_template("flags.html")

# my code end
@app.route("/challenge/<id>") # get all images 
def index(id):
    try:
        # x,target,out = PoW()
        # session["target"] = target
        # session["x"] = x[:13].hex()
        return render_template("index.html",chall_name=CHALL_NAMES[int(id)-1]["image_name"]) #,question=out,pub_key = pub_key
    except Exception as e:
        return str(e)
    

@app.route("/deploy/challenge/<id>",methods=["POST"]) # get all images 
def deploy(id): 
    try:
        print(request)
        # if(request.form['answer'] == None): # check if answer is present
        #     raise  
        # answer = request.form['answer']
        # print(answer,session['target'],flush=True)
        if(1):  # check if answer is correct
            r = requests.post(API_URL+"/api/deploy",json={"image_id":CHALL_NAMES[int(id)-1]["image_name"],"user_id":"admin"}) # deploy container 
            print(r.text)
            print(json.loads(r.text)['port'],flush=True)
            # session['target'] = "chavar"
            return {"id":id,"port":json.loads(r.text)['port'],"timeout":json.loads(r.text)['timeout'],"status":"SUCCESS"},200
        return {"id":id,"status":"FAIL"},400
    except Exception as e:
        print("Error:",str(e))
        return {"id":id,"status":"error"},400
    
# MISC API's

@app.route("/submit/challenge/<name>",methods=["POST"])
def submit(name):
    flag = request.form['flag']
    for chall in CHALL_NAMES:
        if chall["image_name"] == name:
            if(flag == chall['flag']):
                # insert 1 entry in solved challs
                try:
                    solved_challenges = SolvedChallenges.query.filter_by(user_id="user1").all()
                    solve = SolvedChallenges(chall_id=chall['image_name'],solved_chall_name=chall['image_name'],point=chall['point'],user_id="user1")
                    db.session.add(solve)
                    db.session.commit()
                except Exception as e:
                    print("Some Exception Occured in L128: "+str(e))
                    return {"status":"fail"},400
                return {"status":"success"},200
    return {"status":"fail"},400
            
@app.route("/scoreboard")
def scoreboard():
    users = Users.query.all()
    results = []

    for user in users:
        total_points = 0
        for solved_chall in user.solvedChalls:
            total_points += solved_chall.point
        
        # Append the data to the results list
        results.append({
            'user_id': user.user_id,
            'username': user.username,
            'total_points': total_points,
            'solved_challenges': [{
                'chall_id': solved_chall.chall_id,
                'solved_chall_name': solved_chall.solved_chall_name,
                'point': solved_chall.point
            } for solved_chall in user.solvedChalls]
        })

    # Sort the results list in decending order of total points
    results = sorted(results, key=lambda k: k['total_points'], reverse=True)

    # Return the data in JSON format
    return render_template('scoreboard.html',results=results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)