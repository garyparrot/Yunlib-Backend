from Yunlib.Yunlib import Yunlib as YunlibMain
from linebot.models import *

app = YunlibMain('./resource.ini')

@app.onTextReceivce
def say_it(user_id, reply_token, text):
    app.linebot.reply_message(reply_token, TextSendMessage(text))

@app.onPostbackReceive
def postback(user_id, reply_token, data):
    app.linebot.reply_message(reply_token, TextSendMessage(data))

@app.onUserFollow
def say_welcome(user_id, reply_token):
    app.linebot.reply_message(reply_token, TextSendMessage("WELCOME TO HELL"))

@app.onUserUnfollow
def shit(user_id):
    print("user", user_id, "doesn't love you.")
