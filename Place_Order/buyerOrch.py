from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

# card_URL = "http://localhost:5000/card"
order_URL = "http://localhost:5001/"
payment_URL = "http://localhost:5002/"
shipping_URL = "http://localhost:5003/"


@app.route("/place_order", methods=['POST'])
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
                "message": "buyerOrch.py internal error: " + ex_str
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

        # # Inform the error microservice
        # print('\n\n-----Invoking error microservice as order fails-----')
        # invoke_http(error_URL, method="POST", json=order_result)
        # # - reply from the invocation is not used; 
        # # continue even if this invocation fails
        # print("Order status ({:d}) sent to the error microservice:".format(
        #     code), order_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": order_result},
            "message": "Order creation failure sent for error handling."
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

        # # Inform the error microservice
        # print('\n\n-----Invoking error microservice as shipping fails-----')
        # invoke_http(error_URL, method="POST", json=shipping_result)
        # print("Shipping status ({:d}) sent to the error microservice:".format(
        #     code), shipping_result)

        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
                "payment_result": payment_result
            },
            "message": "Simulated payment error sent for error handling."
        }

    # 7. Return created order, payment
    return {
        "code": 201,
        "data": {
            "order_result": order_result,
            "payment_result": payment_result
        }
    }

@app.route("/see-payment/<string:buyer_id>", methods=['GET'])    
def find_by_buyer_id(buyer_id):
    print('\n-----Invoking order microservice-----')
    payment_result = invoke_http(payment_URL + '/payment-new/' + buyer_id, method='GET')
    print('payment_result:', payment_result)
    
    code = payment_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "payment_result": payment_result,
            },
            "message": "You have no order with pending payment."
        })
    
    payments = payment_result["data"]
    order_result = []
    for payment in payments:
        order_id = payment["order_id"]
        order_result_temp = invoke_http(order_URL+"/order/"+order_id,method="GET")
        order_result.append(order_result_temp)
    
    # 7. Return all orders
    return jsonify({
        "code": 200,
        "data": {
            "payment_result": payment_result,
            "order_result": order_result
        }
    })

@app.route("/change-payment-status/<string:payment_id>", method="PUT")
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
                "message": "buyerOrch.py internal error: " + ex_str
            }), 500

def processChangePaymentStatus(payment,payment_id):
    print('\n-----Invoking payment microservice-----')
    payment_result = invoke_http(payment_URL+"/payment/"+payment_id, method='PUT', json=payment)
    print('payment_result:', payment_result)

    # # 4. Record new payment

    # Check the payment result; if a failure, send it to the error microservice.
    code = payment_result["code"]
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"payment_result": payment_result},
            "message": "Payment status change failure sent for error handling."
        }

    # 7. Return created order, payment
    return {
        "code": 201,
        "data": {
            "payment_result": payment_result
        }
    }
    

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)