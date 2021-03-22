from flask import Flask, request, jsonify
from flask_cors import CORS

import os

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# card_URL = "http://localhost:5000/card"
order_URL = "http://localhost:5001/order"
payment_URL = "http://localhost:5002/payment"
shipping_URL = "http://localhost:5003/shipping"


@app.route("/place_order", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            order = request.get_json()
            print("\nReceived an order in JSON:", order)

            # do the actual work
            # 1. Send order info {cart items}
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
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print('\n-----Invoking order microservice-----')
    order_result = invoke_http(order_URL, method='POST', json=order)
    print('order_result:', order_result)

    # # 4. Record new order
    # # record the activity log anyway
    # print('\n\n-----Invoking activity_log microservice-----')
    # invoke_http(activity_log_URL, method="POST", json=order_result)
    # print("\nOrder sent to activity log.\n")
    # # - reply from the invocation is not used;
    # # continue even if this invocation fails

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
        payment_URL, method="POST", json=order_result['data'])
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

@app.route("/see_order/<string:buyer_id>", methods=['GET'])
def find_by_buyer_id(buyer_id):
    print('\n-----Invoking order microservice-----')
    order_result = invoke_http(order_URL + '/' + buyer_id, method='GET')
    print('order_result:', order_result)
    
    code = order_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": order_result,
            },
            "message": "You have not place any order yet."
        }

    # 7. Return all orders
    return {
        "code": 200,
        "data": {
            "order_result": order_result
        }
    }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)