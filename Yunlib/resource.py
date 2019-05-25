import linebot, configparser, os
from .Singleton import Singleton

E_RUNNING_ENVIRONMENT_DYNO = "DYNO"
E_RUNNING_ENVIRONMENT_MACHINE = "MACHINE"

chatBarText = "雲科圖書館 Linebot"
RichMenuSizeX = 2500
RichMenuSizeY = 843
RichMenuAreaX = [61, 811, 1566]
RichMenuAreaY = [0,0,0]
RichMenuAreaSizeW = [700,700,530]
RichMenuAreaSizeH = [843,843,843]
RichMenuSize = linebot.models.RichMenuSize(width=RichMenuSizeX, height=RichMenuSizeY)

Postback_ViewBooks = "ViewBooks"
Postback_NotifyEnable = "EnableNotify"
Postback_NotifyDisable = "DisableNotify"
Postback_AboutUs = "AboutUs"

NotifyMenuName = "NotfiyMenu"
NotifyMenuLabels = [ "檢視我的書目", "到期提示已啟動", "About" ]
NotifyMenuData = [ Postback_ViewBooks, Postback_NotifyDisable, Postback_AboutUs ]
NotifyMenuText = ["查看我借的書", "關閉到期提示", "關於你們"]

NNotifyMenuName = "NotifyDisabledMenu"
NNotifyMenuLabels = [ "檢視我的書目", "到期提示已關閉", "About" ]
NNotifyMenuData = [ Postback_ViewBooks, Postback_NotifyEnable, Postback_AboutUs ]
NNotifyMenuText = ["查看我借的書", "開啟到期提示", "關於你們"]

Render_EmptyBookListHint = "你的書櫃是空的 :)"

DB_USERINFO_TNAME = "userinfo"

# WARNING: THIS IS NOT THE PLACE WHERE YOU CONFIG YOUR PERSONAL DATA
#          PLEASE CONFIG THEM IN './config/resource.ini' FILE
F_CHANNEL_ACCESS_TOKEN = "CHANNEL_ACCESS_TOKEN"
F_CHANNEL_SECRET = "CHANNEL_SECRET"
F_ACCOUNT_ID = "ACCOUNT_ID"
F_ACCOUNT_PASSWORD = "ACCOUNT_PASSWORD"
F_RUNNING_ENVIRONMENT = "RUNNING_ENVIRONMENT"
F_DB_HOST = "DB_HOST"
F_DB_DATABASE = "DB_DATABASE"
F_DB_USER = "DB_USER"
F_DB_PORT = "DB_PORT"
F_DB_PASSWORD = "DB_PASSWORD"
F_DB_TYPE = "DB_TYPE"
F_DB_NAME = "DB_NAME"


class ConfigLoader(metaclass=Singleton):

    def __init__(self, config_file):
        self.parser = configparser.ConfigParser()
        self._load_config(config_file)

    def fetch_config(self,config_name):
        if config_name in os.environ:
            return os.environ[config_name]
        elif self.parser.has_option('Setting', config_name):
            return self.parser['Setting'][config_name]
        else:
            return None

    def _load_config(self ,config_path = './resource.ini'):
        if os.path.isfile(config_path):
            self.parser.read(config_path)

    def db_access_config(self):
        ini_options = {
                "db_type"   : F_DB_TYPE,
                "database"  : F_DB_NAME,
                "dbname"    : F_DB_DATABASE,
                "user"      : F_DB_USER,
                "password"  : F_DB_PASSWORD,
                "host"      : F_DB_HOST,
                "port"      : F_DB_PORT 
                }
        config = {}

        for rel, opt in ini_options.items():
            config[rel] = self.fetch_config(opt)

        return config
