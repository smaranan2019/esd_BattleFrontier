import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@localhost:3306/orderDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

CORS(app)  

class Order(db.Model):
    __tablename__ = 'order'

    order_id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(4,2), nullable=False)
    #status = db.Column(db.String(10), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'order_id': self.order_id,
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'price': self.price,
            #'status': self.status,
            'created': self.created,
            'modified': self.modified
        }

        dto['item'] = []
        for item in self.item:
            dto['item'].append(item.json())
            
        # dto['contact'] = []
        # for ct in self.contact:
        #     dto['contact'].append(ct.json())
        
        return dto


class Item(db.Model):
    __tablename__ = 'item'

    order_id = db.Column(db.ForeignKey(
        'order.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)

    card_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship(
        'Order', primaryjoin='Item.order_id == Order.order_id', backref='item')

    def json(self):
        return {'card_id': self.card_id, 'quantity': self.quantity, 'order_id': self.order_id}
    

# class Contact(db.Model):
#     __tablename__ = 'contact'

#     order_id = db.Column(db.ForeignKey(
#         'order.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)

#     seller_chat_id = db.Column(db.Integer, nullable=False)
#     buyer_chat_id = db.Column(db.Integer, nullable=False)
    
#     order = db.relationship(
#         'Order', primaryjoin='Contact.order_id == Order.order_id', backref='contact')

#     def json(self):
#         return {'seller_chat_id': self.seller_chat_id, 'buyer_chat_id': self.buyer_chat_id, 'order_id': self.order_id}


# @app.route("/order")
# def get_all():
#     orderlist = Order.query.all()
#     if len(orderlist):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "orders": [order.json() for order in orderlist]
#                 }
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no orders."
#         }
#     ), 404


@app.route("/order/<string:order_id>")
def find_by_order_id(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order_id": order_id
            },
            "message": "Order not found."
        }
    ), 404
    
# @app.route("/order-buyer/<string:buyer_id>")
# def find_by_buyer_id(buyer_id):
#     order = Order.query.filter_by(buyer_id=buyer_id)
#     if order:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": order.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "buyer_id": buyer_id
#             },
#             "message": "You have not placed any order."
#         }
#     ), 404
    
# @app.route("/order-seller/<string:seller_id>")
# def find_by_seller_id(seller_id):
#     order = Order.query.filter_by(seller_id=seller_id)
#     if order:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": order.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "data": {
#                 "seller_id": seller_id
#             },
#             "message": "You don't have any order yet."
#         }
#     ), 404


@app.route("/order", methods=['POST'])
def create_order():
    buyer_id = request.json.get('buyer_id',None)
    item = request.json.get('item')
    
    order = Order(buyer_id=buyer_id, price=item['card']['price']*item['quantity'],seller_id=item['card']['seller_id']) #, status='NEW')   
    order.item.append(Item(
        card_id=item['card']['card_id'], quantity=item['quantity']))
    
    # order.contact.append(Contact(
    #     seller_chat_id=item['card']['seller_chat_id'], buyer_chat_id=buyer['buyer_chat_id']))

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500
    
    print(json.dumps(order.json(), default=str)) # convert a JSON object to a string and print
    print()

    return jsonify(
        {
            "code": 201,
            "data": order.json()
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
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
