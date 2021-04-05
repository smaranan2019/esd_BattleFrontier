from flask import Flask, request, jsonify
import telegram

import os

app = Flask(__name__)

TOKEN = "1641597329:AAFVhB4MAHU39OUZs_JhyY0SexezTHwDvIg"
# mainUrl = "https://api.telegram.org/bot1641597329:AAFVhB4MAHU39OUZs_JhyY0SexezTHwDvIg"
# chat_id = "961849285"
bot = telegram.Bot(token=TOKEN)

@app.route("/send-notification", methods=["POST"])
def sendNotif():
    data = request.get_json()

    if "telechat_id" in data:
        telechat_id = data["telechat_id"]
    else:
        telechat_id = "835159639"
        
    if "message" in data:
        message = data["message"]
    else:
        message = "This is a generated text for business user. Some user just paid/ shipped"

    print("#############################################################")
    print(data)
    print("#############################################################")

    try:
        bot.sendMessage(chat_id=telechat_id, text=message)
    except Exception as e:
        return jsonify(
            {
                "code" : 500,
                "message" : "Failed to send notification." + str(e)
            }
        )
    return jsonify(
        {
            "code": 200,
            "message": "Notification has been sent"
        }
    )

# @app.route("/{}".format(TOKEN), methods=["POST"])
# def respond():
#     print("aaaaa")
#     update = telegram.Update.de_json(request.get_json(force=True), bot)

#     print(update)

#     chat_id = update.message.chat.id
#     msg_id = update.message.message_id

#     received_text = update.message.text.encode('utf-8').decode()

#     print(received_text)

#     try:
#         if received_text == "/start":
#             msg = "Hi pls end my existence. My creator not only trash but also suicidal"
#             bot.sendMessage(chat_id=chat_id, text=msg)
#         else:
#             msg = "You have sent a message, but I dont' care. All care about is "
#             bot.sendMessage(chat_id=chat_id, text=msg)
#     except:
#         return "Something went wrong"

#     return "Someone sent something"

# @app.route("/sendNotification", methods=['POST'])
# def sendNotification():
#     data = request.get_json()
#     if (data["status"] == "shipped"):
#         send = urllib.request.urlopen(mainUrl + "sendMessage?")
#         sendData = json.loads(send)
#         return sendData
#     if (data["status"] == "received"):
#         send = urllib.request.urlopen()
#         sendData = json.loads(send)
#         return sendData

# @app.route("/")
# def welcomeMessage():
#     data = request.get_json("https://api.telegram.org/bot1790750890:AAEffcouXbkLWuzRTr100MGtjvgnK84-EgE/getUpdates")
#     msg = "Thank you for adding the BattleFrontier telegram notifciation bot! Do not be worried about getting spammed as we will " \
#           "only send you notifications regarding updates on your order and shipping. Now go catch'em all!"
#     return data.json()

@app.route("/")
def index():
    return "Service is running!"

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for sending telegram message...")
    app.run(host="0.0.0.0", port=5004, debug=True, threaded=True)