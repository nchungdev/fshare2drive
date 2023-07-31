from function import *

ps = myParser()
cf = toDict(ps)

# get data from config
USER_API_URL = cf['API']['user_api_url']
MAIL = cf['Auth']['mail']
PASSWORD = cf['Auth']['password']
USER_AGENT = cf['Auth']['user_agent']
APP_KEY = cf['Auth']['app_key']
GDRIVE_ENABLED = cf['Drive']['gdrive']
GDRIVE_FOLDER_PATH = cf['Drive']['drive_folder_path']

if GDRIVE_ENABLED == '0' or GDRIVE_FOLDER_PATH == '':
    print("------------------------")
    print("┌─────────────────────┐")
    print("| CONFIG GOOGLE DRIVE |")
    print("└─────────────────────┘")
    if GDRIVE_ENABLED == '0':
        GDRIVE_ENABLED = input("1. Do you want to upload to your google drive? (0: no, 1: yes)")
        if GDRIVE_ENABLED == '1':
            ps.set('Drive', 'gdrive', '1')
    if GDRIVE_ENABLED == '1':
        GDRIVE_FOLDER_PATH = input("2. Which place do you want to store files?")
        if GDRIVE_FOLDER_PATH != '':
            ps.set('Drive', 'drive_folder_path', GDRIVE_FOLDER_PATH)
    print("--------> DONE <--------")
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
    print("--------> DONE <--------")
# store config
with open('config.ini', 'w') as f:
    ps.write(f)