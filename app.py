from fileinput import filename
from flask import Flask, render_template, request
import os
from pymongo import MongoClient
from dotenv import load_dotenv

app = Flask(__name__, template_folder="templates", static_folder="static")

load_dotenv('.env')
password = os.environ.get("PASSWORD")
print(password)



connection_string = "mongodb+srv://CSE312_NN:{}@cse312.pezegun.mongodb.net/test".format(password)
client = MongoClient(connection_string)

db = client["CSE312_Game"] #The name of the database is CSE312_Game
#db.create_collection("Game Data") #Method to create a new collection in the CSE312_Game database.



login_collection = db["Login"]





print(connection_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/static/{path}')
def aboutCss(path):
    with open(path) as f:
        return f.read()

@app.route('/game')
def index2():
    return render_template('index2.html')

@app.route('/register', methods=["POST"])
def register():
    uploadData = {}
    uploadData["email"] = request.form.get("email")
    uploadData["password"] = request.form.get("password")
    print(request.form.get("email"))
    print(request.form.get("password"))
    #password not secure right now

    login_collection.insert_one(uploadData)
    return render_template('about.html')

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
