import os
from function import *


def is_file(path):
    return os.path.isfile(path)


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
    if is_file(sys.argv[1]):
        urls = get_url_from_file(sys.argv[1])
    else:
        for index, url in enumerate(sys.argv):
            if index > 0:
                urls.append(sys.argv[index])

fshare_folder = '/content/drive/MyDrive/fshare/'
if check_file_exist(fshare_folder):
    copy_to_drive(fshare_folder + 'config.ini', '')
else:
    create_file(fshare_folder)

CONFIG = Config(config_parser())

urls = process_urls(get_downloaded_info(CONFIG), urls)
# download urls and upload to drive
download(CONFIG, urls)
