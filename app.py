from Yunlib.Yunlib import Yunlib as YunlibMain
import Yunlib.resource as resource
from linebot.models import *

EmptyBookList = {
    "main_title": "B10617008的書目資料",
    "contents": [ ],
    "footer": {"left":"Yunlib", "right":"處理時間:XXX-XX-XX"}
}
BookListExample = {
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

# Yunlib - The module for communicate between server and user
app = YunlibMain('./resource.ini')
flask_app = app.app

@app.onTextReceivce
def say_it(user_id, reply_token, text):
    """ Trigger this function when user sending text """
    if text.startswith('repeat '):
        app.replyText(reply_token,text)

@app.onPostbackReceive
def postback(user_id, reply_token, data):
    """ Trigger this function when user sending postback(for example, press button) """
    # If user press View_Books button
    if data == resource.Postback_ViewBooks:
        app.replyBookList(reply_token,BookListExample)
    # If user press AboutUs button
    elif data == resource.Postback_AboutUs:
        app.pushBookList(user_id,EmptyBookList)
    # If user press Enable_Notification button
    elif data == resource.Postback_NotifyEnable:
        app.updateNotificationSetting(user_id, True)
    # If user press Disable_Notification button
    elif data == resource.Postback_NotifyDisable:
        app.updateNotificationSetting(user_id, False)

@app.onUserFollow
def say_welcome(user_id, reply_token):
    """ Trigger this function when user follow this bot """
    app.pushText(user_id,"Welcome to hell!")
    if app.database.userinfo.query_by_id(user_id) == None:
        app.database.userinfo.insert(user_id)
        app.updateNotificationSetting(user_id, True)
    else:
        old_setting = app.database.userinfo.is_notify_on(user_id)
        app.updateNotificationSetting(user_id, old_setting)

@app.onUserUnfollow
def shit(user_id):
    """ Trigger this function when user block this bot """
    print("user", user_id, "doesn't loves you.")

