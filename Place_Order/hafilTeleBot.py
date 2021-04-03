from flask import Flask, request, jsonify
import telegram

app = Flask(__name__)

TOKEN = "1790750890:AAEffcouXbkLWuzRTr100MGtjvgnK84-EgE"
# mainUrl = "https://api.telegram.org/bot1790750890:AAEffcouXbkLWuzRTr100MGtjvgnK84-EgE"
# chat_id = "961849285"
bot = telegram.Bot(token=TOKEN)

@app.route("/send-notification", methods=["POST"])
def sendNotif():
    data = request.get_json()

    # if "chat_id" in data:
    #     chat_id = data["chat_id"]
    # else:
    chat_id = "961849285"
    
    msg = {
        "Shipped": "Your order has been shipped",
        "Received": "Your order has been received"
    }

    print("#############################################################")
    print(data)
    print("#############################################################")

    try:
        bot.sendMessage(chat_id=chat_id, text="Shipped!")
    except Exception as e:
        return jsonify(
            {
                "code" : 500,
                "message" : str(e)
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

if __name__ == "__main__":
    app.run(port=5300, debug=True, threaded=True)
