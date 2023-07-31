from urllib.parse import unquote

from function import *

FILE_PASSWORD = ''
if len(sys.argv) == 1:
    exit("-> Please include file URL")
elif len(sys.argv) == 3:
    FILE_PASSWORD = sys.argv[2]
FILE_URL = sys.argv[1]

ps = config_parser()
cf = to_dict(ps)

# get data from config
FILE_DL_API_URL = cf['API']['file_dl_api_url']
USER_AGENT = cf['Auth']['user_agent']
APP_KEY = cf['Auth']['app_key']
SESSION_ID = cf['Login']['session_id']
TOKEN = cf['Login']['token']
DRIVE_FOLDER = cf['Drive']['folder_path']

print("-> Connecting to Fshare...")

header = {"Content-Type": "application/json", "accept": "application/json", "User-Agent": USER_AGENT,
          "Cookie": "session_id=" + SESSION_ID}
data = {
    "url": FILE_URL,
    "password": FILE_PASSWORD,
    "token": TOKEN,
    "zipflag": 0
}

r = rq_fshare(url=FILE_DL_API_URL, header=header, data=data)

if r.status_code != 200:
    exit(error_info(r.status_code))

j = request_to_json(r)

DL_URL = j['location']
FILE_NAME = unquote(DL_URL.split('/')[-1])

print("┌─────────────────────────────┐")
print("|          File Info          |")
print("└─────────────────────────────┘")
print("-------------------------------")
print("-> File Name:", FILE_NAME)
print("-> Save Folder: /downloaded")
chunk_download(DL_URL, FILE_NAME)
print("-------------------------------")
print('-> Uploading to Google Drive...')
push_to_drive('downloaded/' + FILE_NAME, DRIVE_FOLDER)
