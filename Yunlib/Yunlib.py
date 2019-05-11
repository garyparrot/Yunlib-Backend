import flask
from flask import Flask, request, abort

from linebot import LineBotApi
from linebot.models import MessageEvent, FollowEvent, PostbackEvent
from linebot.models import TextMessage
from linebot.models import TextSendMessage, FlexSendMessage
from linebot.exceptions import InvalidSignatureError
from linebot import WebhookHandler

from .db import db
from . import resource 
from .resource import ConfigLoader

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
        self.app.add_url_rule('/touchme', view_func=RequestUrl.touch, methods=['GET'])

    def onTextReceivce(self,func):

        @self.handler.add(MessageEvent, message=TextMessage)
        def event_wrapper(event):
            return func(event.source.user_id, event.reply_token, event.message.text)

        return func

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
        return flask.Response('ok', 200)
