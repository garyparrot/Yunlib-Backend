from Yunlib.Yunlib import Yunlib as YunlibMain
import Yunlib.resource as resource
from linebot.models import *

example = {
    "main_title": "B10617008的書目資料",
    "contents": [
        {
            "section_title": "總圖書館",
            "section_subtitle": "共{}本書",
            "booklist" : [
                {"bookname":"Street Nig", "duedate": "108/05/09", "urgent": True},
                {"bookname":"Parrot Party", "duedate": "108/05/09"},
                {"bookname":"Hell bird", "duedate": "108/05/09"},
                {"bookname":"How to exit Vim", "duedate": "108/05/09", "urgent": True},
                {"bookname":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "duedate": "108/05/09"},
                {"bookname":"Python 從入門到放棄", "duedate": "108/05/09"}
            ]
        },
        {
            "section_title": "大麻俱樂部",
            "section_subtitle": "共 3本書",
            "booklist" : [
                {"bookname": "非洲鳥大便", "duedate": "108/08/07"},
                {"bookname": "姑姑姑", "duedate": "108/08/07"},
                {"bookname": "Top Latno", "duedate": "108/08/07"}
            ]
        }
    ],
    "footer": {"left":"有3本書即將到期", "right":"處理時間:XXX-XX-XX"}
}

app = YunlibMain('./resource.ini')

@app.onTextReceivce
def say_it(user_id, reply_token, text):
    if text.startswith('repeat '):
        app.replyText(reply_token,text)

@app.onPostbackReceive
def postback(user_id, reply_token, data):
    if data == resource.Postback_ViewBooks:
        app.replyBookList(reply_token,example)
    elif data == resource.Postback_AboutUs:
        app.pushBookList(user_id,example)

@app.onUserFollow
def say_welcome(user_id, reply_token):
    app.pushText(user_id,"Welcome to hell!")

@app.onUserUnfollow
def shit(user_id):
    print("user", user_id, "doesn't love you.")
