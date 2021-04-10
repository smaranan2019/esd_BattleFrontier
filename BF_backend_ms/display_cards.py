from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

account_URL = environ.get('account_URL') or "http://127.0.0.1:5000/find-user-id/"
card_URL = environ.get('card_URL') or "http://localhost:5005/"

#Display all cards
@app.route("/display-cards", methods=['GET'])
def display_cards():
    print('\n-----Invoking cards microservice-----')
    cards_result = invoke_http(card_URL+'cards', method='GET')

    code = cards_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "cards_result": cards_result,
            },
            "message": "There is no cards in our store at the moment."
        })
    
    cards = cards_result["data"]
    for card in cards["cards"]:
        seller_id = card["card_details"][0]["seller_id"]
        print (account_URL + str(seller_id))
        seller = invoke_http(account_URL + str(seller_id), method="GET")
        
        code = seller["code"]
        if code not in range(200, 300):
            card["card_details"][0]["seller_username"] = "None"
        else:
            card["card_details"][0]["seller_username"] = seller["data"]["username"]
    
    # 7. Return all orders
    return jsonify({
        "code": 200,
        "data": {
            "cards_result": cards_result
        }
    })
    
#Display card by card_id
@app.route("/display-card/<string:card_id>", methods=['GET'])
def display_card_by_id(card_id):
    print('\n-----Invoking cards microservice-----')
    card_result = invoke_http(card_URL+'card/'+card_id, method='GET')
    #print('card_result:', card_result)
    
    code = card_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "card_result": card_result,
            },
            "message": "There is no card with the specified id."
        })
    
    card = card_result["data"]

    seller_id = card["card_details"][0]["seller_id"]
    seller = invoke_http(account_URL + str(seller_id), method="GET")
    
    code = seller["code"]
    if code not in range(200, 300):
        card["card_details"][0]["seller_username"] = "None"
    else:
        card["card_details"][0]["seller_username"] = seller["data"]["username"]
    
    # 7. Return all orders
    return jsonify({
        "code": 200,
        "data": {
            "card_result": card_result
        }
    })
    
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for displaying all cards...")
    app.run(host="0.0.0.0", port=5300, debug=True)