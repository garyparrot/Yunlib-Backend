from Yunlib.Yunlib import Yunlib as YunlibMain
import Yunlib.resource as resource
from linebot.models import *
import crawler, datetime, time, os
from threading import Thread

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

def start_crawler(uid,passwd):
    return crawler.answer(uid,passwd)

def create_booklist(user,booklist):
    def get_footer_left(booklist):
        if len(booklist) == 0:
            return "Yunlib"
        else:
            return "共%d本書" % len(booklist)
    def get_footer_right(booklist):
        time = datetime.datetime.now(tz=UTCPlus8())
        return "處理時間:%d/%d %d:%d" % (time.month, time.day, time.hour, time.minute)

    def parse_content(booklist):
        res = {}
        for book in booklist:
            due = datetime.datetime.fromtimestamp(time.mktime(book['due']),tz=UTCPlus8())
            time_str = "%d/%d/%d" % (due.year-1911, due.month, due.day)
            urgent = (due - datetime.datetime.now(tz=UTCPlus8())).days <= 6
            if not book['library'] in res:
                res[book['library']] = []
            res[book['library']].append({'bookname': book['bookname'], 'duedate': time_str, 'urgent': urgent})
        
        content = []
        for lib, items in res.items():
            content.append({
                'section_title': lib,
                'section_subtitle': '共 %2d本書' % len(items),
                'booklist': items
            })
        
        return content

    blist = {
        "main_title": "%s的書目資料" % user,
        "contents": parse_content(booklist),
        "footer":{
            "left": get_footer_left(booklist),
            "right": get_footer_right(booklist)
        }
    }

    return blist

def run_reminder():
    ids = [item[1] for item in app.database.userinfo.querys()]
    def task():
        # at least one user exist.
        if len(ids) > 0:
            # how many day passed after 1970/1/1
            date = app.database.userinfo.query_by_id(ids[0])[3]
            date = 0 if date == None else date
            last_query = int(date) 
            today = datetime.datetime.now(tz=UTCPlus8())
            current = today.timestamp() // (24*60*60)
            
            # Send msg if we didn't sent the reminder msg today. and only send it after 9:00  
            print("last query", last_query, "current", current)
            if last_query < current and today.hour >= 9 and app.database.userinfo.is_notify_on(ids[0]):
                uid = app.cloader.library_id
                pwd = app.cloader.library_pwd
                raw_booklist, success = start_crawler(uid, pwd)
                if success:
                    result = create_booklist(uid , raw_booklist)
                else:
                    print("shit")
                    return

                # test if there is a book close to the due day.
                alert = False
                for lib in result['contents']:
                    for book in lib['booklist']:
                        if book['urgent'] == True:
                            alert = True
                    lib['booklist'] = list(filter(lambda book: book['urgent'], lib['booklist']))
                    lib['section_subtitle'] = '共 %2d本書' % len(lib['booklist'])
                result['footer']['left'] = "到期提醒"

                if alert:
                    app.pushBookList(ids[0], result)
                    app.pushText(ids[0], "提醒您,上述的書籍即將到期")
                app.database.userinfo.update_note(ids[0], str(int(current)))
    def thread_task():
        while True:
            task()
            time.sleep(60 * 10)

    print("start reminder")
    if app.cloader.fetch_config(resource.F_RUNNING_ENVIRONMENT) == resource.E_RUNNING_ENVIRONMENT_DYNO:
        task()
    else:
        Thread(target=thread_task).run()

# If you interact with this bot all the day, the reminder might not trigger :)
run_reminder()

@app.onTextReceivce
def say_it(user_id, reply_token, text):
    """ Trigger this function when user sending text """
    pass

@app.onPostbackReceive
def postback(user_id, reply_token, data):
    """ Trigger this function when user sending postback(for example, press button) """
    # If user press View_Books button
    if data == resource.Postback_ViewBooks:
        raw_booklist, success = start_crawler(app.cloader.library_id, app.cloader.library_pwd)
        if success:
            booklist = create_booklist(app.cloader.library_id,raw_booklist)
            app.replyBookList(reply_token,booklist)
        else:
            app.replyText("鵝...")
            print(raw_booklist)

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
