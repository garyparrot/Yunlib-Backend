import flask
from flask import Flask, request, abort

from linebot import LineBotApi
from linebot.models import MessageEvent, FollowEvent, PostbackEvent, UnfollowEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage, FlexSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot import WebhookHandler

from .db import db
from . import resource 
from .resource import ConfigLoader
from .models.BookList_Render import BookListRender
from .Awake import send_awake_request

class Yunlib:

    def __init__(self, config_file):
        # Initialize Config loader
        self.cloader = ConfigLoader(config_file)
        # Initialize Web handler
        self.handler = WebhookHandler(self.cloader.fetch_config(resource.F_CHANNEL_SECRET))
        # Initialize Linebot api handler
        self.linebot = LineBotApi(self.cloader.fetch_config(resource.F_CHANNEL_ACCESS_TOKEN))
        # Initialize Database handler
        self.database= db(**self.cloader.db_access_config())

        self.app = Flask(__name__)
        self.app.add_url_rule('/', view_func=RequestUrl.auth_index(self.handler), methods=['POST'])
        
        # Only dyno would send this request to server 
        if resource.E_RUNNING_ENVIRONMENT_DYNO == self.cloader.fetch_config(resource.F_RUNNING_ENVIRONMENT):
            self.app.add_url_rule('/touchme', view_func=RequestUrl.touch, methods=['GET'])
            send_awake_request()

    def onTextReceivce(self,func):

        @self.handler.add(MessageEvent, message=TextMessage)
        def event_wrapper(event):
            return func(event.source.user_id, event.reply_token, event.message.text)

        return func

    def onPostbackReceive(self,func):

        @self.handler.add(PostbackEvent)
        def event_wrapper(event):
            return func(event.source.user_id, event.reply_token, event.postback.data)

        return func
    def onUserFollow(self,func):

        @self.handler.add(FollowEvent)
        def event_wrapper(event):
            return func(event.source.user_id, event.reply_token)

        return func
    def onUserUnfollow(self,func):

        @self.handler.add(UnfollowEvent)
        def event_wrapper(event):
            return func(event.source.user_id)

        return func
    def pushText(self,user_id, message):
        self.linebot.push_message(user_id, TextSendMessage(text=message))

    def pushBookList(self, user_id, booklist, alt_text='[Book list]'):
        render = BookListRender(booklist).Render()
        message = FlexSendMessage(alt_text=alt_text, contents = render)
        self.linebot.push_message(user_id, message)

    def replyText(self,reply_token,message):
        self.linebot.reply_message(reply_token, TextSendMessage(text=message))

    def replyBookList(self, reply_token, booklist, alt_text='[Book list]'):
        render = BookListRender(booklist).Render()
        message = FlexSendMessage(alt_text=alt_text, contents = render)
        self.linebot.reply_message(reply_token, message)

    def changeRichMenu(self, user_id, menu_name):
        if not hasattr(self,'_rich_menus'):
            self._rich_menus = self.linebot.get_rich_menu_list()

        target = [i for i in self._rich_menus  if i.name == menu_name][0]
        self.linebot.link_rich_menu_to_user(user_id, target.rich_menu_id)

    def updateNotificationSetting(self, user_id, boolval):
        try:
            self.database.userinfo.update_notify(user_id, boolval)
            menu_name = resource.NotifyMenuName if boolval else resource.NNotifyMenuName
            self.changeRichMenu(user_id, menu_name)
        except Exception as e:
            raise e


class RequestUrl:
    @classmethod
    def auth_index(cls, handler):
        def index():
            """Linebot Webhook"""
            
            signature = request.headers['X-Line-Signature']
            body = request.get_data(as_text=True)

            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                print("Invalid signature")

            return 'Ok'
        
        return index

    @classmethod
    def touch(cls):
        send_awake_request()
        return flask.Response('ok', 200)

