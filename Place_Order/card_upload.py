import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cardDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Card(db.Model):
    __tablename__ = 'card'

    card_id = db.Column(db.Integer, primary_key=True)
    pokemon_name = db.Column(db.String(255), nullable=False)
    pokemon_type = db.Column(db.String(10), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def json(self):
        dto = {
            'card_id': self.card_id,
            'pokemon_name': self.pokemon_name,
            'pokemon_type': self.pokemon_type,
            'image_path': self.image_path,
            'description': self.description
        }
        dto['card_details'] = []
        for detail in self.card_details:
            dto['card_details'].append(detail.json())       
        return dto

class Card_details(db.Model):
    __tablename__ = 'card_details'

    card_id = db.Column(db.ForeignKey(
        'card.card_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    seller_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(4,2), nullable=False)

    card = db.relationship(
        'Card', primaryjoin='Card_details.card_id == Card.card_id', backref='card_details')

    def json(self):
        return {'seller_id': self.seller_id, 'price': self.price, 'card_id': self.card_id}
    
@app.route('/')
def serviceIsRunning():
    return "Service is running!"

@app.route('/cards')
def show_all_cards():
    cardlist = Card.query.all()
    if len(cardlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "cards": [card.json() for card in cardlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no cards."
        }
    ), 404


@app.route('/addPokemonCard/<string:card_id>', methods=['POST'])
def addPokemonCard(card_id):
    try:
        if (Card.query.filter_by(card_id=card_id).first()):
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

    pokemon_name = request.get_json('pokemon_name', None)
    pokemon_type = request.get_json('pokemon_type', None)
    image_path = request.get_json('image_path', None)
    description = request.get_json('description', None)
    card = Card(pokemon_name=pokemon_name, pokemon_type=pokemon_type, image_path=image_path, description=description)
    
    seller_id = request.get_json('seller_id', None)
    price = request.get_json('price', None)
    card.card_details.append(Card_details(seller_id=seller_id, price=price))

    try:
        db.session.add(card)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(
            {
                "code": 500,
                "data": {
                    "card_id": card_id
                },
                "message": "An error occurred creating the card."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": card.json()
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
    card = Card.query.filter_by(name=data["name"], level=data["level"], price=data["price"])
    if (card):
        # print(type(card))
        print(card)
        return "Card found!"
    else:
        return "Card not found!"

if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage cards ...")
    app.run(host='0.0.0.0', port=5005, debug=True)