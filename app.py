from fileinput import filename
from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import re

app = Flask(__name__, template_folder="templates", static_folder="static")

# load_dotenv('.env')
# password = os.environ.get("PASSWORD")
# print(password)



# connection_string = "mongodb+srv://CSE312_NN:{}@cse312.pezegun.mongodb.net/test".format(password)
client = MongoClient('mongo')

db = client["CSE312_Game"] #The name of the database is CSE312_Game
#db.create_collection("Game Data") #Method to create a new collection in the CSE312_Game database.



login_collection = db["Login"]

score_collection = db["scores"] #Where the scores of the users will be stored once the users are implemented

dummy_collection = db["dummy_scores"] # A collection for testing scores being displayed to the leadboard.







# print(connection_string)
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/signin')
def signin():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/score')
def score():
    uploadData = {}

    for item in dummy_collection.find():  #Testing databse retrieval 
        del item['_id'] #Removes unwanted ID key
        uploadData.update(item)

    return jsonify(uploadData)

@app.route('/static/{path}')
def aboutCss(path):
    with open(path) as f:
        return f.read()

@app.route('/game')
def index2():
    return render_template('game.html')

@app.route('/register', methods=["POST"])
def register():
    uploadData = {}
    uploadData["email"] = request.form.get("email")
    uploadData["password"] = request.form.get("password")
    if (check(uploadData["email"])):
        login_collection.insert_one(uploadData)
        return render_template('about.html')
    #password not secure right now

    else:
        return render_template('index.html')

@app.route('/login',methods=["POST"])
def login():
   uploadData = {}
   uploadData["email"] = request.form.get("email")
   uploadData["password"] = request.form.get("password")
   compare = login_collection.find_one(uploadData)

   if compare == None:
       return render_template("login.html")
    
   else:
       del compare['_id']

       if uploadData == compare:
           return render_template("about.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7878)
