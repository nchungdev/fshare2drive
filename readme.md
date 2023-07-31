# Fshare2Drive - Download, save and upload to Google Drive using Fshare API.

## Introduction

Fshare2Drive is a tool to transfer Fshare file to Google Drive using Fshare API.

## Requirements
- You need to have a VIP Fshare with daily bandwith available account to use this tool (to can download file with high speed).
- A VPS with high speed internet connection (to can upload file to Google Drive with high speed), and can have unlimited bandwith.

## Before install
- Create API app for Fshare: go to [this page](https://www.fshare.vn/api-doc). Click `Get App Key` button, then fill the form and click `Submit` button. You will get `App Key` and `App Secret` for your app via email.

## Installation
- Bellow instruction is for Ubuntu 20.04 and any Debian distro, but you can install on other Linux distro with some changes.
- Update and install Python 3 (`>= 3.6`)

    ```bash
    sudo apt update
    sudo apt install python3 python3-pip git
    ```
- How to use:
## Setup tool
### Bash
```bash
git clone https://github.com/nchungdev/fshare2drive
cd fshare_tool
cp config.ini.example config.ini
pip3 install -r requirements.txt
python3 init_settings.py
python3 login_fshare.py
```
### Colab
```bash
!git clone https://github.com/nchungdev/fshare2drive
!cd fshare_tool
!mv -v fshare_tool/* .
!rm -r fshare_tool
!mv config.ini.example config.ini
!pip3 install -r requirements.txt
!python3 init_settings.py
!python3 login_fshare.py
```
## To upload file from Fshare link to Drive, use:
### Bash
```bash
python3 download.py <url1> <url2>
```
### Colab
```bash
!python3 download.py <url1> <url2>
```