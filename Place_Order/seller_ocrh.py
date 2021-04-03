from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import ampq_setup as amqp_setup 
import pika
import json

import time

app = Flask(__name__)
CORS(app)

shipping_URL = "http://localhost:5003/"
order_URL = "http://localhost:5001/"
order_orch_URL = "http://localhost:5100/"
payment_URL = "http://localhost:5002/"

@app.route('/update-shipping/<string:shipping_id>', methods=["PUT"])
def update_shipping(shipping_id):

    data = request.get_json()

    # print(data)

    if data["shipping_status"] == "REJECTED":
        try:
            shipping_rejected = reject_shipping(data)
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
            
            return jsonify(
                {
                    "code": 200,
                    "data":{
                        shipping_rejected
                    },
                    "message": "Shipping " + data["shipping_id"] + " was rejected by seller" 
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "code" : 500,
                    "message": str(e)
                }
            )

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
                )
            

            order_id = shipping_updated["data"]["shipping_details"][0]["order_id"]
            order_details = invoke_http(order_URL + "order/" + str(order_id))

            message = {
                "code": 200,
                "message": "Order has been shipped!",
                "status": "shipped"
            }

            message = json.dumps(message)

            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="#", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 



            # send_shipping_update = invoke_http(order_orch_URL + "shipping-sent/" + shipping_id)

            # if send_shipping_update["code"] not in range(200, 300):
            #     return jsonify(
            #         {
            #             "code": 404,
            #             "data": {
            #                 "shipping_id": shipping_id
            #             },
            #             "message": "Shipping not found."
            #         }
            #     )

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


def reject_shipping(data):
    
    return 


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
                        "seller_id": seller_id
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

@app.route('/receive-payment-status')
def receive_payment_status():
    payment_data = request.get_json()

    try:
        #TODO: AMQP
        print("a")
    except Exception as e:
        pass
    return "a" 

@app.route('/receive-shipping-status')
def receive_shipping_status():
    shipping_status = request.get_json()
    try:
        #TODO: Invoke the AMQP
        updated_shipping = update_shipping(shipping_status["shipping_id"])
        if update_shipping["code"] not in range(200, 300):
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "shipping_id": shipping_status["shipping_id"]
                    },
                    "message": "Shipping does not exist"
                }
            ), 404
        
        updated_payment = invoke_http(payment_URL + 'payment/' + shipping_status["payment_id"])
        if updated_payment["code"] not in range(200, 300):
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "payment_id": shipping_status["payment_id"]
                    },
                    "message": "Payment does not exist"
                }
            ), 404

        return jsonify(
            {
                "code": 200,
                "data": [
                    updated_payment,
                    updated_shipping
                ],
                "message": "Transaction succeeded"
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code" : 500,
                "message": str(e)
            }
        )

if __name__== "__main__":
    app.run(host='0.0.0.0', port=5200, debug=True)