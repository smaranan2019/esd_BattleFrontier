from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/accountdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    __tablename__ = 'account'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    telehandle = db.Column(db.String(255), nullable=False)
    PaypalEmail = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self,  username, telehandle, PaypalEmail, password):
        # self.user_id = user_id
        self.username = username
        self.telehandle = telehandle
        self.PaypalEmail = PaypalEmail
        self.password = password
    
    def json(self):
        return{
            "user_id": self.UserID,
            "username": self.username,
            "telehandle": self.telehandle,
            "PaypalEmail": self.PaypalEmail,
            "password": self.password
        }

@app.route('/add-user', methods=['POST'])
def addUser():
    data = request.get_json()
    print(data)
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

    user = User(**data)

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

@app.route("/find-user/<string:email>")
def findUser(email):
    user = User.query.filter_by(PaypalEmail=email).first()
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

if __name__ == "__main__":
    app.run(port=5000)
