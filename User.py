from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.String(13), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telegram_id = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, user_id, name, email, telegram_id, phone_number, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.telegram_id = telegram_id
        self.phone_number = phone_number
        self.password = password
    
    def json(self):
        return{
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "telegram_id": self.telegram_id,
            "phone_number": self.phone_number,
            "password": self.password
        }

@app.route('/addUser/<string:user_id>', methods=['POST'])
def addUser(user_id):
    data = request.get_json()
    print(data)
    try:
        if (User.query.filter_by(user_id=user_id).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "user_id": user_id
                    },
                    "message": "User already exists."
                }
            ), 400
    except:
        pass

    user = User(user_id, **data)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_id": user_id
                },
                "message": "An error occurred creating the user."
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            "data": user.json()
        }
    ), 201

@app.route("/findUser/<string:email>")
def findUser(email):
    user = User.query.filter_by(email=email).first()
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
