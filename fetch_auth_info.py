import os
from function import *

CONFIG = Config(config_parser())
    if check_file_exist(CONFIG.fshare_folder):
        CONFIG.copy_of(Config(config_parser(CONFIG.fshare_folder + 'config.ini')))
        commit_config(CONFIG.parser)