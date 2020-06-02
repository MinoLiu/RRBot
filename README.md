# RRBot

![Release](https://github.com/Sean2525/RRBot/workflows/Release/badge.svg?branch=master) ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Sean2525/RRBot) ![GitHub](https://img.shields.io/github/license/sean2525/RRBot?color=blue)

A bot for RR

## For normal user

### Release

- https://github.com/Sean2525/RRBot/releases

### Usage for powershell

```
$ ./rrbot.exe
usage: rrbot.exe [-h] [-l LOGIN_METHOD] [-u USE_TO_UPGRADE] [-p PROFILE] [--poor] [--headless] [--proxy PROXY] [--upgrade_strategy UPGRADE_STRATEGY]
               [--debug DEBUG]

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN_METHOD, --login_method LOGIN_METHOD
                        登入選項: 'GOOGLE'、'FB'、'VK'
  -u USE_TO_UPGRADE, --use_to_upgrade USE_TO_UPGRADE
                        升級道具: 'RRCash'、'GOLD' 預設使用 RRCash, 當金小於4320將會改用RRCash
  -p PROFILE, --profile PROFILE
                        帳戶profile: 預設為'default', 修改可更換帳戶
  --poor                你是窮人, 你買不起高級會員, 你必須手動挖礦、軍演, 可憐哪 我來幫你
  --headless            確定使用者有登入成功後可開啟 將瀏覽器GUI關閉節省資源
  --proxy PROXY         正確格式如下: socks5://localhost:1080, https://localhost:1080
  --upgrade_strategy UPGRADE_STRATEGY
                        三圍100後將按照時間比例來升級 default '2:1:1'
  --debug DEBUG         開啟Debug mod
```

#### 第一次使用請不要開啟 headless mode

```
$ ./rrbot.exe -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash
$ ./rrbot.exe -l FB -p FB_ACCOUNT -u RRCash
```

#### 你買不起高帳

```
$ ./rrbot.exe -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash --poor --upgrade_strategy '2:2:1'
```

#### Use proxy

```
$ ./rrbot.exe -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash --proxy socks5://localhost:1080
```

#### headless mode

```
$ ./rrbot.exe -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash --headless
```

## For developer

### Todo List

- [x] Perk upgrading
- [x] Working
- [x] Military training
- [x] Purchase weapons and produce energy drinks

### Requirement

- python 3+

### Install

```
$ git clone https://github.com/Sean2525/RRBot
$ cd RRBot
$ pip install pipenv
$ pipenv install --dev
```

### Build

```
pipenv run pyinstaller -F -n rrbot.exe main.py
```

### Usage

Let `pipenv run python main.py` replace `rrbot.exe`

```
$ pipenv run python main.py
usage: main.py [-h] [-l LOGIN_METHOD] [-u USE_TO_UPGRADE] [-p PROFILE] [--poor] [--headless] [--proxy PROXY] [--upgrade_strategy UPGRADE_STRATEGY]
               [--debug DEBUG]

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN_METHOD, --login_method LOGIN_METHOD
                        登入選項: 'GOOGLE'、'FB'、'VK'
  -u USE_TO_UPGRADE, --use_to_upgrade USE_TO_UPGRADE
                        升級道具: 'RRCash'、'GOLD' 預設使用 RRCash, 當金小於4320將會改用RRCash
  -p PROFILE, --profile PROFILE
                        帳戶profile: 預設為'default', 修改可更換帳戶
  --poor                你是窮人, 你買不起高級會員, 你必須手動挖礦、軍演, 可憐哪 我來幫你
  --headless            確定使用者有登入成功後可開啟 將瀏覽器GUI關閉節省資源
  --proxy PROXY         正確格式如下: socks5://localhost:1080, https://localhost:1080
  --upgrade_strategy UPGRADE_STRATEGY
                        三圍100後將按照時間比例來升級 default '2:1:1'
  --debug DEBUG         開啟Debug mod
```
