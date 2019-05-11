from Yunlib.Yunlib import Yunlib as YunlibMain
from linebot.models import *

app = YunlibMain('./resource.ini')

@app.onTextReceivce
def say_it(user_id, reply_token, text):
    app.linebot.reply_message(reply_token, TextSendMessage(text))
