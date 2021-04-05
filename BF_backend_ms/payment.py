import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/paymentDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(25), nullable=False, default="NEW")
    #refund_status = db.Column(db.String(25), nullable=False, default="NULL")
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'payment_id': self.payment_id,
            'order_id': self.order_id,
            'payment_status': self.payment_status,
            #'refund_status': self.refund_status,
            'created': self.created,
            'modified': self.modified
        }

        dto['payment_details'] = []
        for detail in self.payment_details:
            dto['payment_details'].append(detail.json())
            
        # dto['contact'] = []
        # for ct in self.contact:
        #     dto['contact'].append(ct.json())
        
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
    

# class Contact(db.Model):
#     __tablename__ = 'contact'

#     payment_id = db.Column(db.ForeignKey(
#         'payment.payment_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)

#     seller_chat_id = db.Column(db.Integer, nullable=False)
#     buyer_chat_id = db.Column(db.Integer, nullable=False)

#     payment = db.relationship(
#         'Payment', primaryjoin='Contact.payment_id == Payment.payment_id', backref='contact')

#     def json(self):
#         return {'seller_chat_id': self.seller_chat_id, 'buyer_chat_id': self.buyer_chat_id, 'payment_id': self.payment_id}


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

@app.route("/payment-release")
def find_all_need_release():
    paymentlist = Payment.query.filter(Payment.payment_status=="RELEASABLE")
    
    if paymentlist.count():
        return jsonify(
            {
                "code": 200,
                "data": [payment.json() for payment in paymentlist]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no payment to release."
        }
    ), 404
    
@app.route("/payment-refundable")
def find_all_need_refund():
    paymentlist = Payment.query.filter(Payment.payment_status=="REFUNDABLE")
    
    if paymentlist.count():
        return jsonify(
            {
                "code": 200,
                "data": [payment.json() for payment in paymentlist]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There is no payment to refund."
        }
    ), 404
    
@app.route("/payment-release/<string:payment_id>")
def find_all_need_release_by_payment_id(payment_id):
    payment = Payment.query.filter(Payment.payment_status=="RELEASABLE", Payment.payment_id==payment_id).first()
    
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
            "message": "There is no payment with the payment_id to release."
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
    
# @app.route("/payment-buyer/<string:buyer_id>")
# def find_by_buyer_id(buyer_id):
#     paymentlist = Payment.query.join(Payment_details, Payment.payment_id == Payment_details.payment_id).filter(Payment_details.buyer_id==buyer_id)
    
#     if paymentlist.count():
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [payment.json() for payment in paymentlist]
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "buyer_id": buyer_id
#             },
#             "message": "You haven't made any payment yet."
#         }
#     ), 404

@app.route("/payment-new-buyer/<string:buyer_id>")
def find_new_by_buyer_id(buyer_id):
    payment = Payment.query.join(Payment_details, Payment.payment_id == Payment_details.payment_id).filter(Payment_details.buyer_id==buyer_id,Payment.payment_status=="NEW").first()
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
    
@app.route("/payment-refund-buyer/<string:buyer_id>")
def find_refund_by_buyer_id(buyer_id):
    paymentlist = Payment.query.join(Payment_details, Payment.payment_id == Payment_details.payment_id).filter(Payment_details.buyer_id==buyer_id,Payment.payment_status=="REFUNDED")
    if paymentlist.count():
        return jsonify(
            {
                "code": 200,
                "data": [payment.json() for payment in paymentlist]
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "buyer_id": buyer_id
            },
            "message": "You don't have any refunded payment yet."
        }
    ), 404
    
# @app.route("/payment-seller/<string:seller_id>")
# def find_by_seller_id(seller_id):
#     paymentlist = Payment.query.join(Payment_details, Payment.payment_id == Payment_details.payment_id).filter(Payment_details.seller_id==seller_id)
    
#     if paymentlist.count():
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [payment.json() for payment in paymentlist]
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "seller_id": seller_id
#             },
#             "message": "You haven't had any payment yet."
#         }
#     ), 404
    
# @app.route("/payment-new-seller/<string:seller_id>")
# def find_new_by_seller_id(seller_id):
#     paymentlist = Payment.query.join(Payment_details, Payment.payment_id == Payment_details.payment_id).filter(Payment_details.seller_id==seller_id, Payment.payment_status=="NEW")
    
#     if paymentlist.count():
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": [payment.json() for payment in paymentlist]
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "seller_id": seller_id
#             },
#             "message": "You haven't had any payment yet."
#         }
#     ), 404


@app.route("/payment", methods=['POST'])
def create_order():
    order_id  = request.json.get('order_id', None)   
    price = request.json.get('price', None)
    payment = Payment(order_id=order_id, payment_status='NEW')#, refund_status='NULL')
         
    buyer_id = request.json.get('buyer_id', None)
    seller_id = request.json.get('seller_id', None)

    payment.payment_details.append(Payment_details(
        buyer_id=buyer_id, seller_id=seller_id, amount=price))
    
    # contact = request.json.get('contact')
    # payment.contact.append(Contact(
    #     seller_chat_id=contact['seller_chat_id'], buyer_chat_id=contact['buyer_chat_id']))

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


@app.route("/payment/<string:payment_id>", methods=['PUT'])
def update_payment(payment_id):
    try:
        payment = Payment.query.filter_by(payment_id=payment_id).first()
        if not payment:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "payment_id": payment_id
                    },
                    "message": "Payment not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['payment_status']:
            payment.payment_status = data['payment_status']
            #NEW, REFUNDABLE, PAID, RELEASABLE, REFUNDED, COMPLETED
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": payment.json()
                }
            ), 201
            
        # elif data['refund_status']:
        #     payment.refund_status = data['refund_status']
        #     db.session.commit()
        #     return jsonify(
        #         {
        #             "code": 201,
        #             "data": payment.json()
        #         }
        #     ), 201
            
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "payment_id": payment_id
                },
                "message": "An error occurred while updating the payment status. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage payments ...")
    app.run(host='0.0.0.0', port=5002, debug=True)