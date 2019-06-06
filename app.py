from Yunlib.Yunlib import Yunlib as YunlibMain
import Yunlib.resource as resource
from linebot.models import *
import datetime, time, os

class UTCPlus8(datetime.tzinfo):
    # can be configured here
    _offset = datetime.timedelta(seconds = 60*60*8)
    _dst = datetime.timedelta(0)
    _name = "+0800"
    def utcoffset(self, dt):
        return self.__class__._offset
    def dst(self, dt):
        return self.__class__._dst
    def tzname(self, dt):
        return self.__class__._name

# Yunlib - The module for communicate between server and user
app = YunlibMain('./resource.ini')
flask_app = app.app

@app.onTextReceivce
def say_it(user_id, reply_token, text):
    """ Trigger this function when user sending text """
    pass

@app.onPostbackReceive
def postback(user_id, reply_token, data):
    """ Trigger this function when user sending postback(for example, press button) """
    # If user press View_Books button
    if data == resource.Postback_ViewBooks:
        pass;
    # If user press AboutUs button
    elif data == resource.Postback_AboutUs:
        app.replyText(reply_token, "Python 作業")
    # If user press Enable_Notification button
    elif data == resource.Postback_NotifyEnable:
        app.updateNotificationSetting(user_id, True)
    # If user press Disable_Notification button
    elif data == resource.Postback_NotifyDisable:
        app.updateNotificationSetting(user_id, False)

@app.onUserFollow
def say_welcome(user_id, reply_token):
    """ Trigger this function when user follow this bot """
    query = app.database.userinfo.querys()
    if len(query) == 0 or user_id in [id[1] for id in query]:
        app.replyText(reply_token,"歡迎你使用Yunlib, %s" % app.cloader.library_id)
        if app.database.userinfo.query_by_id(user_id) == None:
            app.database.userinfo.insert(user_id)
            app.updateNotificationSetting(user_id, True)
        else:
            old_setting = app.database.userinfo.is_notify_on(user_id)
            app.updateNotificationSetting(user_id, old_setting)
    else:
        app.replyText(reply_token,"Yunlib同時間只時服務一位使用者\n想清除上個使用者可嘗試清除教學")

@app.onUserUnfollow
def shit(user_id):
    """ Trigger this function when user block this bot """
    pass
