import configparser
import re
import sys
import os

import requests
from urllib.parse import unquote


# sys func
def exit(err):
    sys.exit(err)


def config_parser(path='config.ini'):
    ps = configparser.ConfigParser()
    ps.read(path)
    return ps


def to_dict(self, get='All'):
    d = dict(self._sections)
    for k in d:
        d[k] = dict(self._defaults, **d[k])
        d[k].pop('__name__', None)
    return d if get == 'All' else d[get]


def error_info(error_code):
    ec = str(error_code)
    i = {
        '405': '-> Wrong Password, please edit correct information config',
        '406': '-> Account not activated',
        '409': '-> Account is locked login',
        '410': '-> Account is locked login',
        '424': '-> You entered wrong password 3 times, please enter again after 10 minutes',
        '201': '-> Not logged in yet! Please rerun login file!'
    }
    return i[ec] if ec in i else "Unknown Error"


def rq_fshare(type='POST', url='', header=None, data=None):
    if data is None:
        data = {}
    if header is None:
        header = {}
    return requests.post(url=url, headers=header, json=data)


def request_to_json(self):
    import json
    return json.loads(json.dumps(self.json()))


def chunk_download(furl, name, folder='downloaded/'):
    import math, enlighten
    url = furl
    file_name = name
    # Should be one global variable
    manager = enlighten.get_manager()
    r = requests.get(url, stream=True)
    assert r.status_code == 200, r.status_code
    dlen = int(r.headers.get('Content-Length', '0')) or 0
    print('-> File Size: ', '{:.2f}'.format(dlen / (2 ** 20) / 1024),
          'GB (' + str(math.ceil(dlen / 2 ** 20)), "MB)")
    with manager.counter(color='green', total=dlen and math.ceil(dlen / 2 ** 20), unit='MiB',
                         leave=False) as ctr, \
            open(folder + file_name, 'wb', buffering=2 ** 24) as f:
        for chunk in r.iter_content(chunk_size=2 ** 20):
            # print(chunk[-16:].hex().upper())
            f.write(chunk)
            ctr.update()
    return file_name


def move_to_drive(file='', path=''):
    os.popen('mv -v ' + " '" + file + "' " + path)
    print('-> Uploaded ' + file + ', ' + ' to ' + path)


def copy_to_drive(file='', path=''):
    os.popen('cp -v ' + " '" + file + "' " + path)
    print('-> Copied ' + file + ', ' + ' to ' + path)


def commit_config(parser):
    with open('config.ini', 'w') as f:
        parser.write(f)


class Config:
    def __init__(self, parser):
        self.parser = parser
        cf = to_dict(parser)
        self.get_folder_list = cf['API']['get_folder_list']
        self.user_api_url = cf['API']['user_api_url']
        self.file_dl_api_url = cf['API']['file_dl_api_url']
        self.fshare_folder = cf['Drive']['fshare_folder']
        self.download_folder = cf['Drive']['download_folder']
        self.app_key = cf['Auth']['app_key']
        self.user_agent = cf['Auth']['user_agent']
        self.mail = cf['Auth']['mail']
        self.password = cf['Auth']['password']
        self.ssid = cf['Login']['session_id']
        self.token = cf['Login']['token']

    def copy_of(self, config):
        self.parser = config.parser
        self.get_folder_list = config.get_folder_list
        self.user_api_url =  config.user_api_url
        self.file_dl_api_url = config.file_dl_api_url
        self.fshare_folder = config.fshare_folder
        self.download_folder = config.download_folder
        self.app_key = config.app_key
        self.user_agent = config.user_agent
        self.mail = config.mail
        self.password =config.password

    def is_valid(self):
        return self.mail != '' and self.password != '' and self.user_agent != '' and self.app_key != ''

    def is_login(self):
        return self.is_valid() and self.ssid != '' and self.token != ''

    def get_download_folder(self):
        if self.download_folder == '':
            print("------------------------")
            self.download_folder = input("Which place do you want to store files?\n")
            if self.download_folder != '':
                self.parser.set('Drive', 'download_folder', self.download_folder)
                commit_config(self.parser)
            else:
                self.download_folder = '/content/drive/MyDrive/Downloaded'
                print("-> Use default Google Drive folder")
        return self.download_folder


def login_fshare(config: Config):
    if not config.is_valid():
        print("------------------------")
        print("┌──────────────────────┐")
        print("| CONFIG FSHARE AUTHEN |")
        print("└──────────────────────┘")
        if config.mail == '':
            config.mail = input("---> Enter Your Mail: ")
            config.parser.set('Auth', 'mail', config.mail)
        if config.password == '':
            config.password = input("---> Enter Your Password: ")
            config.parser.set('Auth', 'password', config.password)
        if config.user_agent == '':
            config.user_agent = input("---> Enter User Agent: ")
            config.parser.set('Auth', 'user_agent', config.user_agent)
        if config.app_key == '':
            config.app_key = input("---> Enter App key: ")
            config.parser.set('Auth', 'app_key', config.app_key)
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
    config.parser.set('Login', 'SESSION_ID', ssid)
    config.parser.set('Login', 'TOKEN', token)
    commit_config(config.parser)

    print("--------> Success <--------")


def is_login_fshare(config: Config):
    return config.is_login() or login_fshare(config)


def is_folder_fshare(url):
    pattern = r"https://www\.fshare\.vn/folder/"
    return re.match(pattern, url) is not None


def is_file_fshare(url):
    pattern = r"https://www\.fshare\.vn/"
    return re.match(pattern, url) is not None


def check_file_exist(file_path):
    """Check if a file exists and create it if it does not exist."""
    if os.path.exists(file_path):
        return True
    else:
        return False


def create_file(file_path):
    """Create a file if it does not exist."""
    if not check_file_exist(file_path):
        with open(file_path, "w") as f:
            f.write("")


def get_url_from_file(file=''):
    urls = []
    try:
        with open(file, 'r') as file:
            for line in file:
                line = line.strip()
                if re.match(r'^https?://\S+', line):
                    urls.append(normalize_url(line))
    except FileNotFoundError:
        return []
    return urls


def can_download(url, downloaded_urls):
    return url not in downloaded_urls


def make_downloaded(downloaded_info, file_name, url):
    if not check_file_exist(downloaded_info):
        create_file(downloaded_info)
    with open(downloaded_info, 'a') as fp:
        fp.write("# %s\n" % file_name)
        fp.write("%s\n" % url)

def normalize_url(url):
    if url.find("?") > 0:
        return url.split("?")[0]
    return url

def normalize_urls(urls):
    rs = []
    for url in urls:
        rs.append(normalize_url(url))
    return rs

def process_urls(downloaded_info, urls):
    if not check_file_exist(downloaded_info):
        create_file(downloaded_info)
    downloaded_urls = get_url_from_file(downloaded_info)
    return list(filter(lambda url: can_download(url, downloaded_urls), urls))


def get_downloaded_info(config):
    return config.fshare_folder + 'downloaded.txt'


def get_urls_from_folder(config, folder_url):
    if not is_login_fshare(config):
        return []
    header = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'User-Agent': config.user_agent,
        'Cookie': 'session_id=' + config.ssid
    }
    data = {
        "url": folder_url,
        "dirOnly": 0,
        "pageIndex": 0,
        "limit": 200,
        "token": config.token
    }
    r = rq_fshare(url=config.get_folder_list, header=header, data=data)
    if r.status_code != 200:
        print(error_info(r.status_code))
        return []
    json = request_to_json(r)
    urls = []
    for obj in json:
        urls.append(normalize_url(obj['furl']))
    return process_urls(get_downloaded_info(config), urls)


def get_direct_download_url(config: Config, url='', password=''):
    if not is_login_fshare(config):
        return url
    header = {
        'Content-Type': 'application/json',
        'accept': 'application/json',
        'User-Agent': config.user_agent,
        'Cookie': 'session_id=' + config.ssid
    }

    data = dict(url=url, password=password, token=config.token, zipflag=0)

    r = rq_fshare(url=config.file_dl_api_url, header=header, data=data)

    if r.status_code != 200:
        print("Skip this URL: {}, caused by: {}".format(url, error_info(r.status_code)))
        return ''

    json = request_to_json(r)
    return normalize_url(json['location'])

def download(config, urls):
    for index, url in enumerate(normalize_urls(urls)):
        print('-> Input Url: ', url)
        if is_folder_fshare(url):
            print("-> It's a Fshare folder link, let's get the list URL....")
            list_url = get_urls_from_folder(config, url)
            if len(list_url) > 0:
                download(config, list_url)
        direct_url = url
        if is_file_fshare(url):
            print("-> It's a Fshare link, let's get the direct download URL....")
            direct_url = get_direct_download_url(config, url)
        if direct_url != '':
            file_name = unquote(direct_url.split('/')[-1])
            print('┌─────────────────────────────┐')
            print('|          File Info          |')
            print('└─────────────────────────────┘')
            print('-------------------------------')
            print('-> Download Url: ', direct_url)
            print('-> File Name:', file_name)
            print('-> Started')
            chunk_download(direct_url, file_name)
            print('-> Downloaded')
            print('-------------------------------')
            move_to_drive('downloaded/' + file_name, config.download_folder)
            print('-> Completed: {0}/{1}'.format(index + 1, len(urls)))
            make_downloaded(get_downloaded_info(config), file_name, url)
        else:
            print('-> Cannot download file from URL: ', url)
