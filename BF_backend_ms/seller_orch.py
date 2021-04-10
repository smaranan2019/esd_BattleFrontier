from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup as amqp_setup 
import pika
import json

import time

app = Flask(__name__)
CORS(app)

account_URL = environ.get('account_URL') or "http://127.0.0.1:5000/find-user-id/"
payment_URL = environ.get('payment_URL') or "http://localhost:5002/"
shipping_URL = environ.get('shipping_URL') or "http://localhost:5003/"

@app.route('/update-shipping/<string:shipping_id>', methods=["PUT"])
def update_shipping(shipping_id):
    data = request.get_json()
    # print(data)
    if data["shipping_status"] == "REJECTED":
        try:
            shipping_rejected = invoke_http(shipping_URL + "shipping-status/" + shipping_id, method="PUT", json=data)
            if shipping_rejected["code"] not in range(200, 300):
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "shipping_id": shipping_id
                        },
                        "message": "Shipping not found."
                    }
                ), 404
                
            payment_id = shipping_rejected["data"]["payment_id"]
            payment = {
                "payment_id": payment_id,
                "payment_status": "REFUNDABLE"
            }
            payment_result = invoke_http(payment_URL+ "payment/" + str(payment_id), method = 'PUT', json=payment)
            print('payment_result:', payment_result)
            
            if payment_result["code"] not in range(200, 300):
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "shipping": shipping_rejected,
                            "payment_id": payment_id 
                        },
                        "message": "Payment cannot be updated."
                    }
                ), 404
                
            return jsonify(
                {
                    "code": 201,
                    "data":{
                        "shipping": shipping_rejected
                    },
                    "message": "Shipping " + str(data["shipping_id"]) + " was rejected by seller" 
                }
            ), 201
        except Exception as e:
            return jsonify(
                {
                    "code" : 500,
                    "message": str(e)
                }
            ), 500

    elif data["shipping_status"] == "SHIPPED":
        try:
            
            shipping_updated = invoke_http(shipping_URL + "shipping-status/" + shipping_id, method="PUT", json=data)

            if shipping_updated["code"] not in range(200, 300):
                return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "shipping_id": shipping_id
                        },
                        "message": "Shipping not found."
                    }
                ), 404         
            
            buyer_id = shipping_updated["data"]["shipping_details"][0]["buyer_id"]
    
            print('\n-----Invoking account microservice-----')
            buyer = invoke_http(account_URL+str(buyer_id), method="GET")
            
            print(buyer)
            
            code = buyer["code"]
            if code not in range(200, 300):
                buyer_chat_id = 835159639 #default chat_id
            else:
                buyer_chat_id = buyer["data"]["telechat_ID"]
            
            message = {
                "telechat_id": buyer_chat_id,
                "message": "You have a new ship on the way!"
            }
            
            message = json.dumps(message)

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="#", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            return jsonify(
                    {
                        "code": 201,
                        "data":{
                            "shipping": shipping_updated
                        }
                    }
                ), 201

        except Exception as e:
            return jsonify(
            {
                "code": 500,
                "message": ". " + str(e)
            }
        ), 500    

if __name__== "__main__":
    app.run(host='0.0.0.0', port=5200, debug=True)