from function import *

ps = config_parser()
cf = to_dict(ps)

# get data from config
USER_API_URL = cf['API']['user_api_url']
MAIL = cf['Auth']['mail']
PASSWORD = cf['Auth']['password']
USER_AGENT = cf['Auth']['user_agent']
APP_KEY = cf['Auth']['app_key']

print("------------------------")
print("┌──────────────────────┐")
print("|    LOGIN TO FSHARE   |")
print("└──────────────────────┘")
print("--------> Starting <--------")
# api-endpoint (using Fshare API V2)
URL = USER_API_URL + "/login"
header = {"Content-Type": "application/json", "accept": "application/json", "User-Agent": USER_AGENT}
data = {
    "user_email": MAIL,
    "password": PASSWORD,
    "app_key": APP_KEY
}

r = rq_fshare(url=URL, header=header, data=data)

sc = r.status_code
if sc != 200:
    print("--------> Failed <--------")
    exit(error_info(sc))
print("--------> Success <--------")
d = request_to_json(r)
token = d["token"]
ssid = d["session_id"]

print("--------> Saving <--------")
ps.set('Login', 'SESSION_ID', ssid)
ps.set('Login', 'TOKEN', token)

with open('config.ini', 'w') as f:
    ps.write(f)

print("--------> Done <--------")
