#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os

import ampq_setup as amqp_setup
import requests
from invokes import invoke_http

from flask import Flask, request, jsonify, make_response
import telegram

app = Flask(__name__)

monitorBindingKey='#'

TOKEN = "1641597329:AAFVhB4MAHU39OUZs_JhyY0SexezTHwDvIg"
bot = telegram.Bot(token=TOKEN)

# @app.route('/send-notification', methods=["POST"])
def sendNotif(data):
    # data = request.get_json()

    # if "chat_id" in data:
    #     chat_id = data["chat_id"]
    # else:
    # chat_id = "961849285"
    chat_id = "961849285"
    
    msg = {
        "Shipped": "Your order has been shipped",
        "Received": "Your order has been received"
    }

    try:
        bot.sendMessage(chat_id=chat_id, text=data["message"])
    except Exception as e:
        return json.dumps({
                "code" : 500,
                "message" : "Failed to send notification." + str(e)
            })
    return json.dumps({
            "code": 200,
            "message": "Notification has been sent"
        })
def receiveNotifLog():
    # with app.app_context():

        amqp_setup.check_setup()
            
        queue_name = 'Notification'
        
        # set up a consumer and start to wait for coming messages
        amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
        #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a notification log by " + __file__)
    processNotifLog(json.loads(body))
    print() # print a new line feed

def processNotifLog(order):
    print("Recording a notification log:")
    print(order)


    notification_sent = sendNotif(order)
    print(notification_sent)


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveNotifLog()
    app.run(port=5004, debug=True, threaded=True)