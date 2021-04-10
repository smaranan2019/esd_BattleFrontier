from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup as amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

account_URL = environ.get('account_URL') or "http://127.0.0.1:5000/find-user-id/"
order_URL = environ.get('order_URL') or "http://127.0.0.1:5001/"
payment_URL = environ.get('payment_URL') or "http://127.0.0.1:5002/"
shipping_URL = environ.get('shipping_URL') or "http://127.0.0.1:5003/"

# Create new order in order.py then create new payment in payment.py
@app.route("/place-order", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)
            result = processPlaceOrder(order)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "buyer_orch.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processPlaceOrder(order):
    # 2. Send the order info {order}
    # Invoke the order microservice
    print('\n-----Invoking order microservice-----')
    order_result = invoke_http(order_URL+"order", method='POST', json=order)
    print('order_result:', order_result)

    # # 4. Record new order
    # Check the order result; if a failure, send it to the error microservice.
    code = order_result["code"]
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure."
        }

    # 5. Send new order to payment
    # Invoke the payment microservice
    print('\n\n-----Invoking payment microservice-----')
    payment_result = invoke_http(
        payment_URL+"payment", method="POST", json=order_result['data'])
    print("payment_result:", payment_result, '\n')

    # Check the payment result; 
    # if a failure, return code 400.
    code = payment_result["code"]
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
                "payment_result": payment_result
            },
            "message": "Payment creation error."
        }

    # 7. Return created order, payment
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "payment_result": payment_result
        }
    }

#Change payment_status from NEW to PAID
@app.route("/change-payment-status/<string:payment_id>", methods=["PUT"])
def change_payment_status(payment_id):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            payment = request.get_json()
            print("\nReceived an payment change in JSON:", payment)
            result = processChangePaymentStatus(payment,payment_id)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "buyer_orch.py internal error: " + ex_str
            }), 500

def processChangePaymentStatus(payment,payment_id):
    print('\n-----Invoking payment microservice-----')
    payment_result = invoke_http(payment_URL+"/payment/"+payment_id, method='PUT', json=payment)
    print('payment_result:', payment_result)

    code = payment_result["code"]
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"payment_result": payment_result},
            "message": "Payment status change failure."
        }
        
    print('\n-----Invoking shipping microservice-----')
    shipping_result = invoke_http(shipping_URL+"/shipping", method='POST', json=payment_result["data"])
    print('shipping_result:', shipping_result)
    
    seller_id = shipping_result["data"]["shipping_details"][0]["seller_id"]
    
    print('\n-----Invoking account microservice-----')
    seller = invoke_http(account_URL+str(seller_id), method="GET")
       
    code = seller["code"]
    if code not in range(200, 300):
        seller_chat_id = "961849285" #default chat_id
    else:
        seller_chat_id = seller["data"]["telechat_ID"]
    
    message = {
        "telechat_id": seller_chat_id,
        "message": "You have a new order to ship!"
    }
            
    # Invoking pikapikachu
    message = json.dumps(message)

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="#", 
    body=message, properties=pika.BasicProperties(delivery_mode = 2))
    
    # 7. Return changed payment, created shipping
    return {
        "code": 201,
        "data": {
            "payment_result": payment_result,
            "shipping_result": shipping_result
        }
    }
    
#Change receive_status in shipping.py from PENDING to RECEIVED
@app.route("/change-receive-status/<string:shipping_id>", methods=["PUT"])
def change_receive_status(shipping_id):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            shipping = request.get_json()
            print("\nReceived a shipping change in JSON:", shipping)
            result = processChangeReceiveStatus(shipping, shipping_id)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "buyerOrch.py internal error: " + ex_str
            }), 500

def processChangeReceiveStatus(shipping,shipping_id):
    print('\n-----Invoking shipping microservice-----')
    shipping_result = invoke_http(shipping_URL+"/receive-status/"+str(shipping_id), method='PUT', json=shipping)
    print('shipping_result:', shipping_result)

    # # 4. Record new payment

    # Check the payment result; if a failure, send it to the error microservice.
    code = shipping_result["code"]
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"shipping_result": shipping_result},
            "message": "Receive status change failure sent for error handling."
        }
        
    payment_id = shipping_result["data"]["payment_id"]
    payment = {
        "payment_id": payment_id,
        "payment_status": "RELEASABLE"
    }
    print('\n-----Invoking payment microservice-----')
    payment_result = invoke_http(payment_URL+"/payment/"+str(payment_id), method='PUT', json=payment)
    print('payment_result:', payment_result)
    
    if payment_result["code"] not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"shipping_result": shipping_result},
            "message": "Receive status change failure sent for error handling."
        }

    # 7. Return changed payment, created shipping
    return {
        "code": 201,
        "data": {
            "shipping_result": shipping_result,
            "payment_result": payment_result
        }
    }
    
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)   
    
