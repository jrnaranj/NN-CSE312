from flask import Flask, render_template
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('.env')
password = os.environ.get("PASSWORD")
print(password)



connection_string = "mongodb+srv://CSE312_NN:{}@cse312.pezegun.mongodb.net/test".format(password)
client = MongoClient(connection_string)

db = client["CSE312_Game"] #The name of the database is CSE312_Game
#db.create_collection("Game Data") #Method to create a new collection in the CSE312_Game database.



print(connection_string)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def index2():
    return render_template('index2.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7878)
