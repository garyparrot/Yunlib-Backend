"""

This file control how this application gettting user defined resource/data.
We will first look up environment variable, then check the './config/resource.ini' file.

If you are running this app on your machine, better config setting via ini file.
If you are running this app on heroku, better config setting via environment var.

Example content of 'example_resource.ini' file already locate in this directory
To set this up, You should it one and name it './config/resource.ini'

** These setting should be readonly during runtime, do not modify their values **

"""
import linebot, configparser, os


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

NotifyMenuName = "NotfiyMenu"
NotifyMenuLabels = [ "檢視我的書目", "到期提示已啟動", "About" ]
NotifyMenuData = [ "ViewBooks", "DisableNotify", "AboutUs" ]
NotifyMenuText = ["查看我借的書", "關閉到期提示", "關於你們"]

NNotifyMenuName = "NotifyDisabledMenu"
NNotifyMenuLabels = [ "檢視我的書目", "到期提示已關閉", "About" ]
NNotifyMenuData = [ "ViewBooks", "EnableNotify", "AboutUs" ]
NNotifyMenuText = ["查看我借的書", "開啟到期提示", "關於你們"]

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



class ConfigLoader:

    def __init__(self, config_file):
        self.parser = configparser.ConfigParser()
        self.load_config(config_file)

    def fetch_config(self,config_name):
        if config_name in os.environ:
            return os.environ[config_name]
        else:
            return self.parser['Setting'][config_name]

    def load_config(self ,config_path = './resource.ini'):
        if os.path.isfile(config_path):
            self.parser.read(config_path)

    def db_access_config(self):
        return {
                "dbname"    : self.fetch_config(F_DB_DATABASE),
                "user"      : self.fetch_config(F_DB_USER),
                "password"  : self.fetch_config(F_DB_PASSWORD),
                "host"      : self.fetch_config(F_DB_HOST),
                "port"      : self.fetch_config(F_DB_PORT) 
                }

