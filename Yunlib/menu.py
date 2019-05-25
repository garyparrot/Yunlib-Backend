from . import resource as resource
from .resource import ConfigLoader

def init_menu(linebot):
    """
    Initialization for linebot
    This function update the content of rich menu 
    This function should be called on the new setup of linebot.  
    """

    # Delete old menu
    for menu in linebot.get_rich_menu_list():
        linebot.delete_rich_menu(menu.rich_menu_id)

    notify_menu = RichMenu(
            size        = resource.RichMenuSize,
            name        = resource.NotifyMenuName,
            chat_bar_text= resource.chatBarText,
            areas       = create_slots(
                    resource.NotifyMenuLabels,
                    resource.NotifyMenuText,
                    resource.NotifyMenuData,
                    x_array = resource.RichMenuAreaX,
                    y_array = resource.RichMenuAreaY,
                    size_x = resource.RichMenuAreaSizeW,
                    size_y = resource.RichMenuAreaSizeH
                ),
            selected    = False
            )
    nnotify_menu = RichMenu(
            size        = resource.RichMenuSize,
            name        = resource.NNotifyMenuName,
            chat_bar_text= resource.chatBarText,
            areas       = create_slots(
                    resource.NNotifyMenuLabels,
                    resource.NNotifyMenuText,
                    resource.NNotifyMenuData,
                    x_array = resource.RichMenuAreaX,
                    y_array = resource.RichMenuAreaY,
                    size_x = resource.RichMenuAreaSizeW,
                    size_y = resource.RichMenuAreaSizeH
                ),
            selected    = False
            )
    id1 = linebot.create_rich_menu(notify_menu)
    id2 = linebot.create_rich_menu(nnotify_menu)

    with open('./misc/icon_notify.png','rb') as f:
        linebot.set_rich_menu_image(id1,"image/png",f)
    with open('./misc/icon_nnotify.png','rb') as f:
        linebot.set_rich_menu_image(id2,"image/png",f)

def create_slots(label_array , text_array, data_array, x_array, y_array , size_x, size_y):
    """Create rich menu entry array"""
    slots = []
    elements = len(label_array)

    if len(label_array) != len(text_array) or len(label_array) != len(data_array):
        raise Exception("Menu Array length should be the same.")

    for i in range(elements):
        b = RichMenuBounds(x_array[i],y_array[i],size_x[i],size_y[i])
        a = PostbackAction(label=label_array[i], text=text_array[i], data= data_array[i])
        slots.append(RichMenuArea(bounds=b,action=a))
    return slots
