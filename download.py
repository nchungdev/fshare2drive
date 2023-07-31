from urllib.parse import unquote

from function import *

urls = []
if len(sys.argv) == 1:
    user_input = input('Enter urls which you want to download: (one or many url distinct by space or \\n)\n')
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

ps = config_parser()
cf = to_dict(ps)

# get data from config
FILE_DL_API_URL = cf['API']['file_dl_api_url']
USER_AGENT = cf['Auth']['user_agent']
APP_KEY = cf['Auth']['app_key']
SESSION_ID = cf['Login']['session_id']
TOKEN = cf['Login']['token']
DRIVE_FOLDER = cf['Drive']['folder_path']

count = 1
total = len(urls)


def get_direct_download_url(path='', password=''):
    if url.startswith('https://www.fshare.vn'):
        # get data from config
        print('-> Connecting to Fshare...')
        header = {
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'User-Agent': USER_AGENT,
            'Cookie': 'session_id=' + SESSION_ID
        }
        data = dict(url=path, password=password, token=TOKEN, zipflag=0)

        r = rq_fshare(url=FILE_DL_API_URL, header=header, data=data)

        if r.status_code != 200:
            print("Skip this URL, caused by: ")
            print(error_info(r.status_code))
            return ''

        json = request_to_json(r)
        return json['location']
    else:
        return url


for url in urls:
    print('-> Input Url: ', url)
    direct_url = get_direct_download_url(url)
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
        push_to_drive('downloaded/' + FILE_NAME, DRIVE_FOLDER)
        print('-> Completed: {0}/{1}'.format(count, total))
        count += 1
    else:
        print('-> Cannot download file from URL: ', url)
