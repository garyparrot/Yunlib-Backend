import sys, os, subprocess, re, hashlib, getpass

# executable
if sys.platform == 'win32':
    heroku = 'heroku.cmd'
elif sys.platform == 'linux':
    heroku = 'heroku'
else:
    heroku = 'heroku'

# test heroku
if subprocess.run([heroku, '--version']).returncode != 0:
    print("heroku not found")
    exit(1)

print("Encoding: ", sys.stdout.encoding)
app_name    = input("輸入你的Application name: ")
account_id  = input('輸入你的圖書館證號: ')
account_pwd = getpass.getpass('輸入你的圖書館密碼: ')
line_token  = getpass.getpass('輸入你的Line Access token: ')
line_secret = getpass.getpass("輸入你的Line Secret: ")

# login heroku
subprocess.run([heroku, 'login'])

appname = 'yunlib-bot-' + app_name
dbname = 'yunlib-bot-db-' + app_name 

subprocess.run([heroku, 'create',appname])
subprocess.run([heroku, 'labs:enable', 'runtime-dyno-metadata','-a',appname])
subprocess.run([heroku, 'addons:create', 'heroku-postgresql:hobby-dev', '-a', appname , '--name', dbname])
subprocess.run([heroku,'git:remote','--app', appname])

# retrive database config
output = subprocess.check_output([heroku, 'config:get', 'DATABASE_URL'])
pattern = r'postgres:\/\/(.*?)\:(.*?)@(.*?):(.*?)\/(.*?)$'
match = re.compile(pattern).search(output.decode(sys.stdout.encoding))

db_username = match.group(1)
db_password = match.group(2)
db_host = match.group(3)
db_port = match.group(4)
db_database = match.group(5)

# setup database config
result = 0
result += subprocess.run([heroku, 'config:set', 'DB_DATABASE=%s' % db_database]).returncode
result += subprocess.run([heroku, 'config:set', 'DB_HOST=%s' % db_host]).returncode
result += subprocess.run([heroku, 'config:set', 'DB_PASSWORD=%s' % db_password]).returncode
result += subprocess.run([heroku, 'config:set', 'DB_PORT=%s' % db_port]).returncode
result += subprocess.run([heroku, 'config:set', 'DB_USER=%s' % db_username]).returncode
result += subprocess.run([heroku, 'config:set', 'DB_TYPE=%s' % "postgresql"]).returncode
result += subprocess.run([heroku, 'config:set', 'RUNNING_ENVIRONMENT=%s' % "DYNO"]).returncode


if not (line_token == line_secret == account_id == account_pwd == ""):
    result += subprocess.run([heroku, 'config:set', 'CHANNEL_ACCESS_TOKEN=%s' % line_token]).returncode
    result += subprocess.run([heroku, 'config:set', 'CHANNEL_SECRET=%s' % line_secret]).returncode
    result += subprocess.run([heroku, 'config:set', 'ACCOUNT_ID=%s' % account_id]).returncode
    result += subprocess.run([heroku, 'config:set', 'ACCOUNT_PASSWORD=%s' % account_pwd]).returncode
else:
    print("Warning: 沒有提供帳號和Line token等資訊")

if result != 0:
    print("failed to config some setting.")
    exit(0)

subprocess.run(['git', 'push', 'heroku', 'master'])
domain = subprocess.check_output([heroku, 'domains', '--app', appname]).decode(sys.stdout.encoding).split('\n')[1]
print("https://%s" % domain)
print("上述網址為你的Heroku app的domain name") 
print("設定這個網址到你的line bot webhook")
