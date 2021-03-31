from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

import time

app = Flask(__name__)
CORS(app)

shipping_URL = "http://localhost:5003/"
order_URL = "http://localhost:5001/"

@app.route('/update-shipping/<string:shipping_id>', methods=["PUT"])
def update_shipping(shipping_id):

    data = request.get_json()

    try:
        shipping_updated = invoke_http(shipping_URL + "shipping/" + shipping_id, method="PUT", json=data)
        
        if shipping_updated["code"] not in range(200, 300):
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "shipping_id": shipping_id
                    },
                    "message": "Shipping not found."
                }
            )

        order_id = shipping_updated["shipping_details"]["order_id"]
        order_details = invoke_http(order_URL + "order/" + order_id)
        
        return jsonify(
                {
                    "code": 200,
                    "data": [
                        shipping_updated,
                        order_details
                        ]
                }
            ), 200

    except Exception as e:
        return jsonify(
        {
            "code": 500,
            "message": ". " + str(e)
        }
    ), 500    

@app.route('/get-shippings-categorized/<string:seller_id>')
def get_shipping_categorized(seller_id):
    
    categorized_shippings = {
        "PENDING" : [],
        "SENT-PENDING" : [],
        "SENT-RECEIVED": []
    }

    try: 
        shippings = invoke_http(shipping_URL + "shipping/" + seller_id)
        if shippings["code"] not in range(200, 300):
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "seller_d": seller_id
                    },
                    "message": "You haven't had any sent shipping yet."
                }
            ), 404
        
        for shipping in shippings:
            if shipping["shipping_status"] == "PENDING":
                categorized_shippings["PENDING"].append(shipping)
            elif shipping["shipping_status"] == "SENT" and shipping["receive_status"] == "PENDING":
                categorized_shippings["SENT-PENDING"].append(shipping)
            elif shipping["shipping_status"] == "SENT" and shipping["receive_status"] == "RECEIVED":
                categorized_shippings["SENT-RECEIVED"].append(shipping)
        
        return jsonify({
            "code": 200,
            "data": categorized_shippings
        }), 200

    except Exception as e:
        return jsonify(
        {
            "code": 500,
            "message": ". " + str(e)
        }
    ), 500    