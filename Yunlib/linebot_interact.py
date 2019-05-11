"""
These function used to interact with user.
"""
import Yunlib.resource as resource
from Yunlib.SLinebot import SLinebot
from Yunlib.models.box_render import box_render
from linebot.models import MessageEvent, TextSendMessage
from linebot.models import BubbleContainer 

access_token = resource.fetch_config(resource.F_CHANNEL_ACCESS_TOKEN)
SLinebot(access_token)
linebot = SLinebot.getInstance()

def push_text(user_id, message):
    """Send message to specified user"""
    linebot.push_message(user_id, TextSendMessage(text=message))

def reply_text(reply_token, message):
    """Reply message to specified user"""
    linebot.reply_message(reply_token, TextSendMessage(text=message))

def reply_book_info(reply_token, book_info)
    """Reply current book statistics"""    
    render = box_render.BookStatRender(book_info).Render()
    message = FlexSendMessage(alt_text='[Book query]', contents = render)
    linebot.reply_message(reply_token, message)

def push_book_info(user_id, book_info) 
    """Push current book statistics"""    
    render = box_render.BookStatRender(book_info).Render()
    message = FlexSendMessage(alt_text='[Book query]', contents = render)
    linebot.push_message(user_id, message)

_rich_menus = None

def ChangeUserRichMenu(user_id, menu_name):
    global _rich_menus
    if _rich_menus == None:
        _rich_menus = linebot.get_rich_menu_list()

    target = [i for i in _rich_menus if i.name == menu_name][0]
    linebot.link_rich_menu_to_user(user_id, target.rich_menu_id)

