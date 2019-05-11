"""
Provide a few function for main program.
"""

__HookUserTexting = []
__HookUserPostback = []
__HookUserFollow = []

def HookUserText(func):
    __HookUserTexting.append(func)
    return func

def HookUserPostback(func):
    __HookUserPostback.append(func)
    return func

def HookUserFollow(func):
    __HookUserFollow.append(func)
    return func

def OnTextingEvent(user_id, message):
    for f in __HookUserTexting:
        f(user_id, message)

def OnPostbackEvent(user_id, data):
    for f in __HookUserPostback:
        f(user_id, data)

def OnFollowEvent(user_id):
    for f in __HookUserFollow:
        f(user_id)
