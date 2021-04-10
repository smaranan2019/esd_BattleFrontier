from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import json

app = Flask(__name__)
CORS(app)

payment_URL = environ.get('payment_URL') or "http://127.0.0.1:5002/"
shipping_URL = environ.get('shipping_URL') or "http://127.0.0.1:5003/"

#Change payment_status from REFUNDABLE to REFUNDED
@app.route("/change-payment-refund-status/<string:payment_id>", methods=["PUT"])
def change_payment_refund_status(payment_id):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            payment = request.get_json()
            print("\nReceived an payment change in JSON:", payment)
            result = processChangePaymentReleaseStatus(payment,payment_id)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "business_orch.py internal error: " + ex_str
            }), 500

def processChangePaymentRefundStatus(payment,payment_id):
    print('\n-----Invoking payment microservice-----')
    payment_result = invoke_http(payment_URL+"/payment/"+payment_id, method='PUT', json=payment)
    print('payment_result:', payment_result)
    
    if payment_result["code"] not in range(200,300):
        return {
            "code": 500,
            "data": {"payment_result": payment_result},
            "message": "Payment status change failure."
        }
    return {
        "code": 201,
        "data": {"payment_result": payment_result}
    }

#Change paymment_status from RELEASABLE to COMPLETED and receive_status from RECEIVED to COMPLETED
@app.route("/change-payment-release-status/<string:payment_id>", methods=["PUT"])
def change_payment_release_status(payment_id):
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            payment = request.get_json()
            print("\nReceived an payment change in JSON:", payment)
            result = processChangePaymentReleaseStatus(payment,payment_id)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "business_orch.py internal error: " + ex_str
            }), 500

def processChangePaymentReleaseStatus(payment,payment_id):
    print('\n-----Invoking payment microservice-----')
    payment_result = invoke_http(payment_URL+"/payment/"+payment_id, method='PUT', json=payment)
    print('payment_result:', payment_result)

    code = payment_result["code"]
    if code not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"payment_result": payment_result},
            "message": "Payment status change failure sent for error handling."
        }
        
    print('\n-----Invoking shipping microservice-----')
    shipping_result_1 = invoke_http(shipping_URL+"/shipping-payment-id/"+payment_id, method='GET')
    print('shipping_results:', shipping_result_1)
    
    if shipping_result_1["code"] not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"payment_result": payment_result,
                     "shipping_result": shipping_result_1},
            "message": "Payment status change failure."
        }
        
    shipping_id =  shipping_result_1["data"]["shipping_id"]
    shipping = {
        "shipping_id": shipping_id,
        "receive_status": "COMPLETED"
    }

    print('\n-----Invoking shipping microservice-----')
    shipping_result_2 = invoke_http(shipping_URL+"/receive-status/"+str(shipping_id), method='PUT', json=shipping)
    print('shipping_result:', shipping_result_2)
    
    if shipping_result_2["code"] not in range(200, 300):
        # 7. Return error
        return {
            "code": 500,
            "data": {"payment_result": payment_result,
                     "shipping_result": shipping_result_2},
            "message": "Payment status change failure."
        }

    # 7. Return changed payment, created shipping
    return {
        "code": 201,
        "data": {
            "payment_result": payment_result,
            "shipping_result": shipping_result_2
        }
    }
    
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for changing the payment status...")
    app.run(host="0.0.0.0", port=5600, debug=True)   