from urllib.parse import unquote

from function import *


class Config:
    def __init__(self, cf):
        self.mail = cf['Auth']['mail']
        self.password = cf['Auth']['password']
        self.ssid = cf['Login']['session_id']
        self.token = cf['Login']['token']
        self.user_api_url = cf['API']['user_api_url']
        self.file_dl_api_url = cf['API']['file_dl_api_url']
        self.user_agent = cf['Auth']['user_agent']
        self.app_key = cf['Auth']['app_key']
        self.drive_folder = cf['Drive']['folder_path']

    def is_valid(self):
        return self.mail != '' & self.password == '' & self.user_agent != '' & self.app_key == ''

    def is_login(self):
        return self.is_valid() & self.ssid != '' & self.token != ''


urls = []
if len(sys.argv) == 1:
    user_input = input(
        'Enter urls which you want to download: (one or many url distinct by space or \\n)\n')
    urls = user_input.split(' ')
    if len(urls) > 0:
        print('-> Start downloading')
    else:
        urls = user_input.split('\n')
        if len(urls) > 0:
            print('-> Start downloading')
        else:
            exit('-> Must input at least one url')
elif len(sys.argv) > 1:
    for index, url in enumerate(sys.argv):
        if index > 0:
            urls.append(sys.argv[index])

parser = config_parser()
CONFIG = Config(to_dict(parser))


def is_login_fshare(config: Config):
    if config.is_login():
        return True

    if not config.is_valid():
        print("------------------------")
        print("┌──────────────────────┐")
        print("| CONFIG FSHARE AUTHEN |")
        print("└──────────────────────┘")
        if config.mail == '':
            config.mail = input("---> Enter Your Mail: ")
            parser.set('Auth', 'mail', config.mail)
        if config.password == '':
            config.password = input("---> Enter Your Password: ")
            parser.set('Auth', 'password', config.password)
        if config.user_agent == '':
            config.user_agent = input("---> Enter User Agent: ")
            parser.set('Auth', 'user_agent', config.user_agent)
        if config.app_key == '':
            config.app_key = input("---> Enter App key: ")
            parser.set('Auth', 'app_key', config.app_key)
        print("--------> Done <--------")

    print("------------------------")
    print("┌──────────────────────┐")
    print("|    LOGIN TO FSHARE   |")
    print("└──────────────────────┘")
    print("--------> Starting <--------")
    # api-endpoint (using Fshare API V2)
    login_url = config.user_api_url + "/login"
    header = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "User-Agent": config.user_agent
    }
    data = {
        "user_email": config.mail,
        "password": config.password,
        "app_key": config.app_key
    }

    r = rq_fshare(url=login_url, header=header, data=data)

    sc = r.status_code
    if sc != 200:
        print("--------> Failed <--------")
        exit(error_info(sc))
    d = request_to_json(r)
    token = d["token"]
    ssid = d["session_id"]
    if token == '' or ssid == '':
        return False
    config.token = token
    config.ssid = ssid
    parser.set('Login', 'SESSION_ID', ssid)
    parser.set('Login', 'TOKEN', token)

    with open('config.ini', 'w') as f:
        parser.write(f)

    print("--------> Success <--------")
    return True


def get_direct_download_url(config: Config, path='', password=''):
    if url.startswith('https://www.fshare.vn'):
        if not is_login_fshare(config):
            return url
        print('-> Connecting to Fshare...')
        header = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'User-Agent': config.user_agent,
            'Cookie': 'session_id=' + config.ssid
        }
        data = dict(url=path, password=password, token=config.token, zipflag=0)

        r = rq_fshare(url=config.file_dl_api_url, header=header, data=data)

        if r.status_code != 200:
            print("Skip this URL, caused by: ")
            print(error_info(r.status_code))
            return ''

        json = request_to_json(r)
        return json['location']
    else:
        return url


if CONFIG.drive_folder == '':
    print("------------------------")
    CONFIG.drive_folder = input("Which place do you want to store files?")
    if CONFIG.drive_folder != '':
        parser.set('Drive', 'folder_path', CONFIG.drive_folder)
    else:
        CONFIG.drive_folder = '/content/drive/MyDrive/'
        print("-> Use default Google Drive folder")
    print("------------------------")

for index, url in enumerate(urls):
    print('-> Input Url: ', url)
    direct_url = get_direct_download_url(CONFIG, url)
    if direct_url != '':
        FILE_NAME = unquote(direct_url.split('/')[-1])
        print('┌─────────────────────────────┐')
        print('|          File Info          |')
        print('└─────────────────────────────┘')
        print('-------------------------------')
        print('-> Download Url: ', direct_url)
        print('-> File Name:', FILE_NAME)
        print('-> Started')
        chunk_download(direct_url, FILE_NAME)
        print('-> Downloaded')
        print('-------------------------------')
        push_to_drive('downloaded/' + FILE_NAME, CONFIG.drive_folder)
        print('-> Completed: {0}/{1}'.format(index + 1, len(urls)))
    else:
        print('-> Cannot download file from URL: ', url)
