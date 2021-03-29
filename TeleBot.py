import requests
import time
list = ['Hi there, welcome to pokemon battle frontier', 'Hot singles in your area want to meet you! :"))))', 'Alright wots all this then']

token = '1738348275:AAHdhqyX3eXg3WskyUUnnxaOLOWvmNTlAEw'
chat_id = '37579573'


for msg in list:
    base_URL = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+chat_id+"&text='{}'".format(msg)
    requests.get(base_URL)
    time.sleep(5)

#https://api.telegram.org/bot1738348275:AAHdhqyX3eXg3WskyUUnnxaOLOWvmNTlAEw/sendMessage?chat_id=-514712203&text='Hello World'


# url = 'https://api.telegram.org/bot1738348275:AAHdhqyX3eXg3WskyUUnnxaOLOWvmNTlAEw/getUpdates'

# import urllib, json
# import urllib.request
# response = urllib.request.urlopen(url)
# data = json.loads(response.read())
# print(data)