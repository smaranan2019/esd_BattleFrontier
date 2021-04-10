#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os

import amqp_setup as amqp_setup 
import telegram

monitorBindingKey='#'

TOKEN = "1641597329:AAFVhB4MAHU39OUZs_JhyY0SexezTHwDvIg"
bot = telegram.Bot(token=TOKEN)

def sendNotif(data):

    if "telechat_id" in data:
        telechat_id = data["telechat_id"]
    else:
        telechat_id = "835159639" #default telechat_id
        
    if "message" in data:
        message = data["message"]
    else:
        message = "This is a generated text for business user. Some user just paid/ shipped."

    print("#############################################################")
    print(data)
    print("#############################################################")

    try:
        bot.sendMessage(chat_id=telechat_id, text=message)
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