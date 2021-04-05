import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/shippingDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Shipping(db.Model):
    __tablename__ = 'shipping'

    shipping_id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, nullable=False)
    shipping_status = db.Column(db.String(10), nullable=False)
    receive_status = db.Column(db.String(10), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'shipping_id': self.shipping_id,
            'payment_id': self.payment_id,
            'shipping_status': self.shipping_status,
            'receive_status': self.receive_status,
            'created': self.created,
            'modified': self.modified
        }

        dto['shipping_details'] = []
        for detail in self.shipping_details:
            dto['shipping_details'].append(detail.json())
            
        # dto['contact'] = []
        # for ct in self.contact:
        #     dto['contact'].append(ct.json())
        
        return dto


class Shipping_details(db.Model):
    __tablename__ = 'shipping_details'

    shipping_id = db.Column(db.ForeignKey(
        'shipping.shipping_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    buyer_id = db.Column(db.Integer, nullable=False)

    shipping = db.relationship(
        'Shipping', primaryjoin='Shipping_details.shipping_id == Shipping.shipping_id', backref='shipping_details')

    def json(self):
        return {'order_id': self.order_id, 'seller_id': self.seller_id, 'buyer_id': self.buyer_id, 'shipping_id': self.shipping_id}
    

# class Contact(db.Model):
#     __tablename__ = 'contact'

#     shipping_id = db.Column(db.ForeignKey(
#         'shipping.shipping_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)

#     seller_chat_id = db.Column(db.Integer, nullable=False)
#     buyer_chat_id = db.Column(db.Integer, nullable=False)

#     shipping = db.relationship(
#         'Shipping', primaryjoin='Contact.shipping_id == Shipping.shipping_id', backref='contact')

#     def json(self):
#         return {'seller_chat_id': self.seller_chat_id, 'buyer_chat_id': self.buyer_chat_id, 'shipping_id': self.shipping_id}


@app.route("/shipping")
def get_all():
    shippinglist = Shipping.query.all()
    if len(shippinglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippings": [shipping.json() for shipping in shippinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no shippings."
        }
    ), 404


@app.route("/shipping/<string:shipping_id>")
def find_by_shipping_id(shipping_id):
    shipping = Shipping.query.filter_by(shipping_id=shipping_id).first()
    if shipping:
        return jsonify(
            {
                "code": 200,
                "data": shipping.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "shipping_id": shipping_id
            },
            "message": "Shipping not found."
        }
    ), 404
    
@app.route("/shipping-payment-id/<string:payment_id>")
def find_by_payment_id(payment_id):
    shipping = Shipping.query.filter_by(payment_id=payment_id).first()
    if shipping:
        return jsonify(
            {
                "code": 200,
                "data": shipping.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "payment_id": payment_id
            },
            "message": "Shipping not found."
        }
    ), 404
    
# @app.route("/shipping/<string:buyer_id>")
# def find_by_buyer_id(buyer_id):
#     shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.buyer_id==buyer_id)
    
#     if len(shippinglist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "shippings": [shipping.json() for shipping in shippinglist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "buyer_id": buyer_id
#             },
#             "message": "You haven't made any shipping yet."
#         }
#     ), 404
    
# @app.route("/shipping-new-buyer/<string:buyer_id>")
# def find_new_by_buyer_id(buyer_id):
#     shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.buyer_id==buyer_id,Shipping.shipping_status=="PENDING")
    
#     if len(shippinglist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "shippings": [shipping.json() for shipping in shippinglist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "buyer_id": buyer_id
#             },
#             "message": "You haven't made any shipping yet."
#         }
#     ), 404
    
@app.route("/shipping-sent-buyer/<string:buyer_id>")
def find_sent_by_buyer_id(buyer_id):
    shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.buyer_id==buyer_id,Shipping.shipping_status=="SHIPPED",Shipping.receive_status=="PENDING")
    
    if shippinglist.count():
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippings": [shipping.json() for shipping in shippinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "buyer_id": buyer_id
            },
            "message": "You haven't had any sent shipping yet."
        }
    ), 404
    
@app.route("/shipping-received-buyer/<string:buyer_id>")
def find_received_by_buyer_id(buyer_id):
    shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.buyer_id==buyer_id,Shipping.shipping_status=="SHIPPED",Shipping.receive_status=="RECEIVED")
    
    if shippinglist.count():
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippings": [shipping.json() for shipping in shippinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "buyer_id": buyer_id
            },
            "message": "You haven't received any shipping yet."
        }
    ), 404
    
# @app.route("/shipping/<string:seller_id>")
# def find_by_seller_id(seller_id):
#     shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.seller_id==seller_id)
    
#     if shippinglist.count():
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "shippings": [shipping.json() for shipping in shippinglist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "seller_id": seller_id
#             },
#             "message": "You haven't had any shipping yet."
#         }
#     ), 404
    
@app.route("/shipping-new-seller/<string:seller_id>")
def find_new_by_seller_id(seller_id):
    shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.seller_id==seller_id, Shipping.shipping_status=="PENDING", Shipping.receive_status=="PENDING")
    
    if shippinglist.count():
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippings": [shipping.json() for shipping in shippinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "seller_id": seller_id
            },
            "message": "You haven't had any shipping yet."
        }
    ), 404
    
@app.route("/shipping-sent-seller/<string:seller_id>")
def find_sent_by_seller_id(seller_id):
    shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.seller_id==seller_id, Shipping.shipping_status=="SHIPPED", Shipping.receive_status=="PENDING")
    
    if shippinglist.count():
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippings": [shipping.json() for shipping in shippinglist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": {
                "seller_id": seller_id
            },
            "message": "You haven't had any shipping yet."
        }
    ), 404

@app.route("/shipping-complete-seller/<string:seller_id>")
def find_received_by_seller_id(seller_id):
    shippinglist = Shipping.query.join(Shipping_details, Shipping.shipping_id == Shipping_details.shipping_id).filter(Shipping_details.seller_id==seller_id, Shipping.shipping_status=="SHIPPED",Shipping.receive_status=="COMPLETED")
    
    if shippinglist.count():
        return jsonify(
            {
                "code": 200,
                "data": {
                    "shippings": [shipping.json() for shipping in shippinglist]
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": {
                "seller_id": seller_id
            },
            "message": "You haven't had any shipping yet."
        }
    ), 404

@app.route("/shipping", methods=['POST'])
def create_order():
    payment_id  = request.json.get('payment_id', None)   
    shipping = Shipping(payment_id=payment_id, shipping_status='PENDING', receive_status='PENDING')
    
    order_id = request.json.get('order_id', None) 
    payment_details = request.json.get('payment_details')
    print(payment_details)

    shipping.shipping_details.append(Shipping_details(
        order_id=order_id, buyer_id=payment_details[0]['buyer_id'], seller_id=payment_details[0]['seller_id']))
    
    # contact = request.json.get('contact')
    # shipping.contact.append(Contact(
    #     seller_chat_id=contact['seller_chat_id'], buyer_chat_id=contact['buyer_chat_id']))

    try:
        db.session.add(shipping)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the shipping. " + str(e)
            }
        ), 500
    
    print(json.dumps(shipping.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": shipping.json()
        }
    ), 201


@app.route("/shipping-status/<string:shipping_id>", methods=['PUT'])
def update_shipping(shipping_id):
    try:
        shipping = Shipping.query.filter_by(shipping_id=shipping_id).first()
        if not shipping:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "shipping_id": shipping_id
                    },
                    "message": "Shipping not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['shipping_status']:
            shipping.shipping_status = data['shipping_status']
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": shipping.json()
                }
            ), 201
            
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "shipping_id": shipping_id
                },
                "message": "An error occurred while updating the shipping status. " + str(e)
            }
        ), 500
        
@app.route("/receive-status/<string:shipping_id>", methods=['PUT'])
def update_receive(shipping_id):
    try:
        shipping = Shipping.query.filter_by(shipping_id=shipping_id).first()
        if not shipping:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "shipping_id": shipping_id
                    },
                    "message": "Shipping not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['receive_status']:
            shipping.receive_status = data['receive_status']
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": shipping.json()
                }
            ), 201
            
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "shipping_id": shipping_id
                },
                "message": "An error occurred while updating the shipping status. " + str(e)
            }
        ), 500

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage shippings ...")
    app.run(host='0.0.0.0', port=5003, debug=True)