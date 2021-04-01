from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

account_URL = "http://127.0.0.1:5000/find-user-id/"
card_URL = "http://localhost:5005/cards"

@app.route("/display-cards", methods=['GET'])
def display_cards():
    print('\n-----Invoking cards microservice-----')
    cards_result = invoke_http(card_URL, method='GET')
    #print('cards_result:', cards_result)
    
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
    
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for displaying all cards...")
    app.run(host="0.0.0.0", port=5300, debug=True)