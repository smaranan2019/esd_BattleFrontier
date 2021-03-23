from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/esdProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class PokemonCard(db.Model):
    __tablename__ = 'PokemonCard'

    card_id = db.Column(db.String(13), primary_key=True)
    seller_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(255))
    image = db.Column(db.String(255))
    price = db.Column(db.String(255))

    def __init__(self, card_id, seller_id, name, level, image, price):
        self.card_id = card_id
        self.seller_id = seller_id
        self.name = name
        self.level = level
        self.image = image
        self.price = price

    def json(self):
        return {
            "card_id": self.card_id,
            "seller_id": self.seller_id,
            "name": self.name,
            "level": self.level,
            "image": self.image,
            "price": self.price
        }

@app.route('/')
def serviceIsRunning():
    return "Service is running!"

@app.route('/addPokemonCard/<string:card_id>', methods=['POST'])
def addPokemonCard(card_id):
    try:
        if (PokemonCard.query.filter_by(card_id=card_id).first()):
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "card_id": card_id
                    },
                    "message": "Card already exists."
                }
            ), 400
    except: pass

    data = request.get_json()
    pokemon_card = PokemonCard(card_id, **data)

    try:
        db.session.add(pokemon_card)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "data": {
                    "card_id": card_id
                },
                "message": "An error occurred creating the book."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": pokemon_card.json()
        }
    ), 201

@app.route("/findPokemonCard")
def findPokemon():
    data = request.get_json()
    # DataModel:
    # {
    #     "name": name,
    #     "level": level,
    #     "price": price
    # }
    print(data)
    card = PokemonCard.query.filter_by(name=data["name"], level=data["level"], price=data["price"])
    if (card):
        # print(type(card))
        print(card)
        return "Card found!"
    else:
        return "Card not found!"

if __name__ == "__main__":
    app.run(port=5100, debug=True)