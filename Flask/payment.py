import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    # seller_id = db.Column(db.Integer, nullable=False)
    # price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'status': self.status,
            'created': self.created,
            'modified': self.modified
        }

        dto['payment_details'] = self.payment_details.json()
        dto['contact'] = self.contact.json()
        
        return dto


class Payment_details(db.Model):
    __tablename__ = 'payment_details'

    payment_id = db.Column(db.ForeignKey(
        'payment.payment_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    buyer_id = db.Column(db.Integer, nullable=False)

    payment = db.relationship(
        'Payment', primaryjoin='Payment_details.payment_id == Payment.payment_id', backref='payment_details')

    def json(self):
        return {'amount': self.amount, 'seller_id': self.seller_id, 'buyer_id': self.buyer_id, 'payment_id': self.payment_id}
    

class Contact(db.Model):
    __tablename__ = 'contact'

    payment_id = db.Column(db.ForeignKey(
        'payment.payment_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)

    seller_chat_id = db.Column(db.Integer, nullable=False)
    buyer_chat_id = db.Column(db.Integer, nullable=False)

    # order_id = db.Column(db.String(36), db.ForeignKey('order.order_id'), nullable=False)
    # order = db.relationship('Order', backref='order_item')
    payment = db.relationship(
        'Payment', primaryjoin='Contact.payment_id == Payment.payment_id', backref='contact')

    def json(self):
        return {'seller_chat_id': self.seller_chat_id, 'buyer_chat_id': self.buyer_chat_id, 'payment_id': self.payment_id}


@app.route("/payment")
def get_all():
    paymentlist = Payment.query.all()
    if len(paymentlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payments": [payment.json() for payment in paymentlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments."
        }
    ), 404


@app.route("/payment/<string:payment_id>")
def find_by_payment_id(payment_id):
    payment = Payment.query.filter_by(payment_id=payment_id).first()
    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "payment_id": payment_id
            },
            "message": "Payment not found."
        }
    ), 404
    
@app.route("/payment/<string:buyer_id>")
def find_by_buyer_id(buyer_id):
    payment = Payment.query.join(Payment_details, Payment.payment_id == Payment_details.payment_id).filter(Payment_details.buyer_id==buyer_id)
    
    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "buyer_id": buyer_id
            },
            "message": "You haven't made any payment yet."
        }
    ), 404
    
@app.route("/payment/<string:seller_id>")
def find_by_seller_id(seller_id):
    payment = Payment.query.join(Payment_details, Payment.payment_id == Payment_details.payment_id).filter(Payment_details.seller_id==seller_id)
    
    if payment:
        return jsonify(
            {
                "code": 200,
                "data": payment.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "seller_id": seller_id
            },
            "message": "You haven't had any payment yet."
        }
    ), 404


@app.route("/payment", methods=['POST'])
def create_order():
    order_id  = request.json.get('order_id', None)   
    payment = Payment(order_id=order_id, amount=price, status='NEW')
    
    price = request.json.get('price', None) 
    buyer_id = request.json.get('buyer_id', None)
    seller_id = request.json.get('seller_id', None)

    payment.payment_details.append(Payment_details(
        buyer_id=buyer_id, seller_id=seller_id, amount=price))
    
    contact = request.json.get('contact')
    payment.contact.append(Contact(
        seller_chat_id=contact['seller_chat_id'], buyer_chat_id=contact['buyer_chat_id']))

    try:
        db.session.add(payment)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the payment. " + str(e)
            }
        ), 500
    
    print(json.dumps(payment.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": payment.json()
        }
    ), 201


# @app.route("/order/<string:order_id>", methods=['PUT'])
# def update_order(order_id):
#     try:
#         order = Order.query.filter_by(order_id=order_id).first()
#         if not order:
#             return jsonify(
#                 {
#                     "code": 404,
#                     "data": {
#                         "order_id": order_id
#                     },
#                     "message": "Order not found."
#                 }
#             ), 404

#         # update status
#         data = request.get_json()
#         if data['status']:
#             order.status = data['status']
#             db.session.commit()
#             return jsonify(
#                 {
#                     "code": 200,
#                     "data": order.json()
#                 }
#             ), 200
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "order_id": order_id
#                 },
#                 "message": "An error occurred while updating the order. " + str(e)
#             }
#         ), 500


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage payments ...")
    app.run(host='0.0.0.0', port=5002, debug=True)