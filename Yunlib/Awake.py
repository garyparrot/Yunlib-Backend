import os, requests

def send_awake_request():
    target = 'https://script.google.com/macros/s/AKfycbw4kteL5W0dXhK9X6RrYSB-WhIs8cZhMpFO45W6SV_MAB2NYuwc/exec'
    site = "https://{}.herokuapp.com/touchme".format(os.environ['HEROKU_APP_NAME'])

    requests.post(target, data=site);