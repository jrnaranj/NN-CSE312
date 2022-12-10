import json
from fileinput import filename
from flask import Flask, render_template, request, jsonify, redirect
import os
import logging
from threading import Lock
import re
from fileinput import filename

from game_session import GameSession
from dotenv import load_dotenv
from flask import Flask, render_template, request, make_response
from flask_sock import Sock
from pymongo import MongoClient
import random
import bcrypt
import secrets
import hashlib
import string

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}

socket = Sock(app)

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


games = {}
user_to_game: dict[int, GameSession] = {}
open_game: int = -1
open_mut: Lock = Lock()

users = []

def check_for_user(auth):
    db_auth = None

  

    if auth != None:
        hashed_auth = hashlib.sha256(auth.encode()).hexdigest()
        db_auth = login_collection.find_one({"auth_token": hashed_auth})

        if db_auth != None:
            return True
    
    else:
        return False

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
   db_auth = None
   auth = request.cookies.get('auth_token')

   if auth != None:
       hashed_auth = hashlib.sha256(auth.encode()).hexdigest()
       db_auth = login_collection.find_one({"auth_token": hashed_auth})

   if db_auth != None:
       return render_template('signedin.html',user=(db_auth["email"]).replace('<',"&lt;").replace('>',"&gt;"))
    
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

@app.route('/profile')
def profile():
    auth = request.cookies.get('auth_token')

    if auth == None:   #Checks if an auth token has been set
        return render_template("profile_invalid.html")
        
    return render_template('profilepage.html')

@app.route('/score')
def score():
    uploadData = {}

    for item in dummy_collection.find():  #Testing databse retrieval 
        del item['_id'] #Removes unwanted ID key
        uploadData.update(item)

    return jsonify(uploadData)


@app.route('/score-history1',  methods=['GET', 'POST'])
def score_history():

   db_auth = None
   auth = request.cookies.get('auth_token')
   username = None
   score = None

   if auth != None:
       hashed_auth = hashlib.sha256(auth.encode()).hexdigest()
       db_auth = login_collection.find_one({"auth_token": hashed_auth})
       score_cur = dummy_collection.find({db_auth['email']:{}})

       for i in score_cur:
           score = i
       username = db_auth['email']

   if username == None:
       return render_template("profile_invalid.html")

   uploadData = {"name":username, "wins": score}

   return jsonify(uploadData)

@app.route('/static/{path}')
def aboutCss(path):
    with open(path) as f:
        return f.read()

@app.route('/game')
def index2():
    open_mut.acquire()
    gameID = random.randint(0, 100000)
    global open_game
    if open_game >= 0:
        gameID = open_game
        open_game = -1
    else:
        while gameID in games.keys():
            gameID = random.randint(0, 100000)
        open_game = gameID
    open_mut.release()

    if gameID in games:

        user_add = "User" + str(random.randint(0, 10000))

        if check_for_user(request.cookies.get('auth_token')) == True:
            auth = request.cookies.get('auth_token')
            hashed_auth = hashlib.sha256(auth.encode()).hexdigest()
            user_data = login_collection.find_one({"auth_token": hashed_auth})

            if user_data != None:
                user_add = user_data["email"]
            

        user = games[gameID].add_user(str(user_add))

        if user == None:
            resp = redirect("/")
            return resp
    else:
        games[gameID] = GameSession() 
        user_add = "User" + str(random.randint(0, 10000))

        if check_for_user(request.cookies.get('auth_token')) == True:
            auth = request.cookies.get('auth_token')
            hashed_auth = hashlib.sha256(auth.encode()).hexdigest()
            user_data = login_collection.find_one({"auth_token": hashed_auth})

            if user_data !=  None:
                user_add = user_data["email"]

        user = games[gameID].add_user(str(user_add))
    resp = make_response(render_template('game.html', gameID=gameID))
    if user:
        user_to_game[user] = gameID
        resp.set_cookie('username', user)
        resp.set_cookie('game_id', str(gameID))
    return resp



@socket.route('/websocket')
def socketRoutine(ws):
    logging.warning("Socket connected")
    user = request.cookies.get('username') #temp
    game: GameSession = games[user_to_game[user]]
    while True:
        data = ws.receive()
        if data == 'close' or game.users == None:
            ws.send(json.dumps({"messageType": "sorry"}))
            logging.warning("Closing socket")
            for u in game.users:
                user_to_game.pop(u)
            game.free_game()
            games.pop(game.id)
            ws.close()
            break
        jdata = json.loads(data)
        if jdata["messageType"] == "rpsChoice":
            winner = game.store_choice(user, jdata["messageChoice"])
            if winner == "":
                ws.send(json.dumps({"messageType": "sorry"}))
                #this message type isn't allowed currently
                continue
            result = {
                "messageType": "rpsResult",
                "winner": winner
            }

            ws.send(json.dumps(result))
            game.reset_choices()

@app.route('/register', methods=["POST"])
def register():
    
    uploadData = {}
    uploadData["email"] = request.form.get("email")
    if (login_collection.find_one({"email":request.form.get("email")}) == None):
        pass_bytes = request.form.get("password").encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(pass_bytes, salt)
        uploadData["password"] = hashed_pass
    #if (check(uploadData["email"])):
        login_collection.insert_one(uploadData)
        dummy_collection.insert_one({uploadData["email"]: 0})
        return redirect("/signin")
    #initialize a score
    else:
        return redirect("/signup")



    #else:
    #    return render_template('index.html')

@app.route('/login',methods=["POST"])
def login():


   resp = make_response(render_template('profilepage.html'))
   uploadData = {}
   uploadData["email"] = request.form.get("email")
   uploadData["password"] = request.form.get("password")
   compare = login_collection.find_one({"email": uploadData["email"]}) #Finds the dictionary in the database with the credentials for this email.


   alphabet = string.ascii_letters + string.digits
   auth_token = ''.join(secrets.choice(alphabet) for i in range(10))
   hashed_token = hashlib.sha256(auth_token.encode()).hexdigest() 



   if compare == None:
       return render_template("login.html")
    
   db_password = compare.get("password")
   result = bcrypt.checkpw(uploadData["password"].encode('utf-8'), db_password) # Returns a boolean (whether or not password matches the one in the database)

   if uploadData["email"] == compare["email"] and result == True: # If email and passwords match, set auth token.
       resp.set_cookie('auth_token', auth_token)
       login_collection.update_one({'email': uploadData['email']},{"$set":{'auth_token': hashed_token}})
       del compare['_id']
       return resp
    
   else:
        return render_template("login.html")






if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7878)
    # socket.run(app, debug=True, host="0.0.0.0", port=7878)
