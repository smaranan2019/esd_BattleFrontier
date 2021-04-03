from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

display_card_URL = "http://127.0.0.1:5300/display-card/"
order_URL = "http://127.0.0.1:5001/order/"
payment_URL = "http://127.0.0.1:5002/"
shipping_URL = "http://127.0.0.1:5003/"

@app.route("/display-cards-payment-buyer/<string:buyer_id>", methods=['GET'])
def display_cards_payment_buyer(buyer_id):
    print('\n-----Invoking payment microservice-----')
    payment_result = invoke_http(payment_URL+'payment-new-buyer/'+buyer_id, method='GET')
    print('payments_result:', payment_result)
    
    code = payment_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "payment_result": payment_result
            },
            "message": "There is no payments in our store at the moment."
        })
    
    payment = payment_result["data"]

    order_id = payment["order_id"]
    order = invoke_http(order_URL + str(order_id), method="GET")
    
    code = order["code"]
    if code not in range(200, 300):
        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "payment_result": payment_result
            },
            "message": "There is no payments in our store at the moment."
        })
    else:
        payment["card_id"] = order["data"]["item"][0]["card_id"]
        
    card_id = payment["card_id"]
    card_display = invoke_http(display_card_URL+str(card_id), method="GET")
    
    if card_display["code"] not in range(200, 300):
        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "payment_result": payment_result
            },
            "message": "There is no payments in our store at the moment."
        })
    else:
        payment["card_display"] = card_display["data"]["card_result"]["data"]
    
    # 7. Return all orders
    return jsonify({
        "code": 200,
        "data": {
            "payment_result": payment_result
        }
    })
    
@app.route("/display-cards-refund-buyer/<string:buyer_id>", methods=['GET'])
def display_cards_refund_buyer(buyer_id):
    print('\n-----Invoking payment microservice-----')
    payments_result = invoke_http(payment_URL+'payment-refund-buyer/'+buyer_id, method='GET')
    print('payments_result:', payments_result)
    
    code = payments_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "payments_result": payments_result
            },
            "message": "There is no payments in our store at the moment."
        })
    
    payments = payments_result["data"]
    
    for payment in payments:

        order_id = payment["order_id"]
        order = invoke_http(order_URL + str(order_id), method="GET")
        
        code = order["code"]
        if code not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "payments_result": payments_result
                },
                "message": "There is no payments in our store at the moment."
            }), 400
        else:
            payment["card_id"] = order["data"]["item"][0]["card_id"]
            
        card_id = payment["card_id"]
        card_display = invoke_http(display_card_URL+str(card_id), method="GET")
        
        if card_display["code"] not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "payment_results": payments_result
                },
                "message": "There is no payments in our store at the moment."
            }), 400
        else:
            payment["card_display"] = card_display["data"]["card_result"]["data"]
    
    # 7. Return all orders
    return jsonify({
        "code": 200,
        "data": {
            "payment_results": payments_result
        }
    })
    
@app.route("/display-cards-shipping-buyer/<string:buyer_id>", methods=['GET'])
def display_cards_shipping_buyer(buyer_id):
    print('\n-----Invoking shipping microservice-----')
    shippings_result = invoke_http(shipping_URL+'shipping-sent-buyer/'+buyer_id, method='GET')
    print('shippings_result:', shippings_result)
    
    code = shippings_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "shippings_result": shippings_result
            },
            "message": "There is no shippings for you at the moment :("
        }), 400
    
    shippings = shippings_result["data"]["shippings"]
    
    for shipping in shippings:
        
        payment_id = shipping["payment_id"]
        payment = invoke_http(payment_URL+"payment/"+str(payment_id), method="GET")
        
        code = payment["code"]
        
        if code not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "shippings_result": shippings_result
                },
                "message": "There is no shippings for you at the moment :("
            }), 400
        else:
            shipping["payment_details"] = payment["data"]["payment_details"]
        
        order_id = shipping["shipping_details"][0]["order_id"]
        order = invoke_http(order_URL + str(order_id), method="GET")
        
        code = order["code"]
        if code not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "shippings_result": shippings_result
                },
                "message": "There is no shippings for you at the moment :("
            }), 400
        else:
            shipping["card_id"] = order["data"]["item"][0]["card_id"]
            
        card_id = shipping["card_id"]
        card_display = invoke_http(display_card_URL+str(card_id), method="GET")
        
        if card_display["code"] not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "shippings_result": shippings_result
                },
                "message": "There is no payments in our store at the moment."
            }), 400
        else:
            shipping["card_display"] = card_display["data"]["card_result"]["data"]
    
    # 7. Return all orders
    return jsonify({
        "code": 200,
        "data": {
            "shippings_result": shippings_result
        }
    })
    
@app.route("/display-cards-complete-buyer/<string:buyer_id>", methods=['GET'])
def display_cards_complete_buyer(buyer_id):
    print('\n-----Invoking shipping microservice-----')
    shippings_result = invoke_http(shipping_URL+'shipping-received-buyer/'+buyer_id, method='GET')
    print('shippings_result:', shippings_result)
    
    code = shippings_result["code"]
    if code not in range(200, 300):

        # 7. Return error
        return jsonify({
            "code": 400,
            "data": {
                "shippings_result": shippings_result
            },
            "message": "You have not completed any order."
        }), 400
    
    shippings = shippings_result["data"]["shippings"]
    
    for shipping in shippings:
        
        payment_id = shipping["payment_id"]
        payment = invoke_http(payment_URL+"payment/"+str(payment_id), method="GET")
        
        code = payment["code"]
        
        if code not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "shippings_result": shippings_result
                },
                "message": "You have not completed any order."
            }), 400
        else:
            shipping["payment_details"] = payment["data"]["payment_details"]
        
        order_id = shipping["shipping_details"][0]["order_id"]
        order = invoke_http(order_URL + str(order_id), method="GET")
        
        code = order["code"]
        if code not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "shippings_result": shippings_result
                },
                "message": "You have not completed any order."
            }), 400
        else:
            shipping["card_id"] = order["data"]["item"][0]["card_id"]
            
        card_id = shipping["card_id"]
        card_display = invoke_http(display_card_URL+str(card_id), method="GET")
        
        if card_display["code"] not in range(200, 300):
            # 7. Return error
            return jsonify({
                "code": 400,
                "data": {
                    "shippings_result": shippings_result
                },
                "message": "You have not completed any order."
            }), 400
        else:
            shipping["card_display"] = card_display["data"]["card_result"]["data"]
    
    # 7. Return all orders
    return jsonify({
        "code": 200,
        "data": {
            "shippings_result": shippings_result
        }
    })
    
# @app.route("/display-card/<string:card_id>", methods=['GET'])
# def display_card_by_id(card_id):
#     print('\n-----Invoking cards microservice-----')
#     card_result = invoke_http(card_URL+'card/'+card_id, method='GET')
#     #print('card_result:', card_result)
    
#     code = card_result["code"]
#     if code not in range(200, 300):

#         # 7. Return error
#         return jsonify({
#             "code": 400,
#             "data": {
#                 "card_result": card_result,
#             },
#             "message": "There is no card with the specified id."
#         })
    
#     card = card_result["data"]

#     seller_id = card["card_details"][0]["seller_id"]
#     seller = invoke_http(account_URL + str(seller_id), method="GET")
    
#     code = seller["code"]
#     if code not in range(200, 300):
#         card["card_details"][0]["seller_username"] = "None"
#     else:
#         card["card_details"][0]["seller_username"] = seller["data"]["username"]
    
#     # 7. Return all orders
#     return jsonify({
#         "code": 200,
#         "data": {
#             "card_result": card_result
#         }
#     })
    
# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for displaying all cards...")
    app.run(host="0.0.0.0", port=5400, debug=True)