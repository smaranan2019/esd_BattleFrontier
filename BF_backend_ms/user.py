from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/accountDB'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/accountDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    __tablename__ = 'account'

    User_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    telehandle = db.Column(db.String(255), nullable=False)
    telechat_ID = db.Column(db.String(255), nullable=False, default="961849285")
    Paypal_Email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self,  username, telehandle, telechat_ID, Paypal_Email, password):
        # self.user_id = user_id
        self.username = username
        self.telehandle = telehandle
        self.telechat_ID = telechat_ID
        self.Paypal_Email = Paypal_Email
        self.password = password
    
    def json(self):
        return{
            "user_id": self.User_ID,
            "username": self.username,
            "telehandle": self.telehandle,
            "telechat_ID":self.telechat_ID,
            "Paypal_Email": self.Paypal_Email,
            "password": self.password
        }

@app.route('/add-user', methods=['POST'])
def addUser():
    data = request.get_json()
    print(data)

    if "@" in data["telehandle"]:
        data["telehandle"] = data["telehandle"].replace("@", "")

    updates = requests.get("https://api.telegram.org/bot1641597329:AAFVhB4MAHU39OUZs_JhyY0SexezTHwDvIg/getUpdates")

    updates_json = updates.json()

    chat_id = ""

    for item in updates_json["result"]:
        if item["message"]["chat"]["username"] == data["telehandle"]:
            chat_id = item["message"]["chat"]["id"]
    
    data["telechat_ID"] = chat_id

    try:
        existing_user = User.query.filter_by(Username=data["username"]).first() 
        if (existing_user):
            return jsonify(
                {
                    "code": 400,
                    "message": "User already exists."
                }
            ), 400
    except:
        pass

    user = User(username=data["username"], telehandle=data["telehandle"], telechat_ID=data["telechat_ID"], Paypal_Email=data["Paypal_email"], password=data["password"])

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the user."
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201
    
@app.route('/login-user', methods=['POST'])
def checkUser():
    data = request.get_json()
    print(data)
    existing_user = User.query.filter(User.username==data["username"],User.password==data["password"]).first() 
    if (existing_user):
        return jsonify(
            {
                "code": 200,
                "data": existing_user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404
        
@app.route("/find-user-id/<string:User_ID>")
def find_user_by_id(User_ID):
    user = User.query.filter_by(User_ID=User_ID).first()
    if user:
        return jsonify(
            {
                "code": 200,
                "data": user.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404
    
# @app.route("/find-user/<string:email>")
# def findUser(email):
#     user = User.query.filter_by(Paypal_Email=email).first()
#     if user:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": user.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "User not found."
#         }
#     ), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
