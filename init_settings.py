from function import *

ps = config_parser()
cf = to_dict(ps)

# get data from config
USER_API_URL = cf['API']['user_api_url']
MAIL = cf['Auth']['mail']
PASSWORD = cf['Auth']['password']
USER_AGENT = cf['Auth']['user_agent']
APP_KEY = cf['Auth']['app_key']
GDRIVE_FOLDER_PATH = cf['Drive']['folder_path']

if GDRIVE_FOLDER_PATH == '':
    print("------------------------")
    print("┌──────────────────────┐")
    print("| CONFIG GOOGLE DRIVE  |")
    print("└──────────────────────┘")
    GDRIVE_FOLDER_PATH = input("Which place do you want to store files?")
    if GDRIVE_FOLDER_PATH != '':
        ps.set('Drive', 'folder_path', GDRIVE_FOLDER_PATH)
    print("--------> Done <--------")
if MAIL == '' or PASSWORD == '' or USER_AGENT == '' or APP_KEY == '':
    print("------------------------")
    print("┌──────────────────────┐")
    print("| CONFIG FSHARE AUTHEN |")
    print("└──────────────────────┘")
    if MAIL == '':
        mail = input("---> Enter Your Mail: ")
        ps.set('Auth', 'mail', mail)
    if PASSWORD == '':
        pw = input("---> Enter Your Password: ")
        ps.set('Auth', 'password', pw)
    if USER_AGENT == '':
        ua = input("---> Enter User Agent: ")
        ps.set('Auth', 'user_agent', ua)
    if APP_KEY == '':
        app_key = input("---> Enter App key: ")
        ps.set('Auth', 'app_key', app_key)
    print("--------> Done <--------")
# store config
with open('config.ini', 'w') as f:
    ps.write(f)