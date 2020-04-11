# RRBot

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Sean2525/RRBot) ![GitHub](https://img.shields.io/github/license/sean2525/RRBot?color=blue)

A bot for RR

## Requirement

- python 3.8+
- chrome 81

## Todo List

- [x] Perk upgrading
- [x] Working
- [x] Military training
- [x] Weapon replenishment and energy drinks

## Install

```
$ git clone https://github.com/Sean2525/RRBot
$ cd RRBot
$ pip install pipenv
$ pipenv install --dev
```

## Usage

```
$ pipenv run python main.py
# or ./rrbot.exe
usage: main.py [-h] [-l LOGIN_METHOD] [-u USE_TO_UPGRADE] [-p PROFILE] [--upgrade_perk UPGRADE_PERK] [-f] [--headless] [--proxy PROXY]

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN_METHOD, --login_method LOGIN_METHOD
                        登入選項: 'GOOGLE'、'FB'、'VK'
  -u USE_TO_UPGRADE, --use_to_upgrade USE_TO_UPGRADE
                        升級道具: 'RRCash'、'GOLD' 預設使用 RRCash
  -p PROFILE, --profile PROFILE
                        帳戶profile: 預設為'default', 修改可更換帳戶
  --upgrade_perk UPGRADE_PERK
                        生級指定選項 'STR'、'EDU'、'END' 不指定將會使用Discord社群推薦的配點
  -f, --first_login     預設為False, True將會等待60秒讓使用者登入
  --poor                你是窮人, 你買不起高級會員, 你必須手動挖礦、軍演, 可憐哪 我來幫你
  --headless            預設為False, True將會停用瀏覽器GUI (由於headless chrome目前有bug無法共通user-data所以目前無法使用)
  --proxy PROXY         請先去確認proxy活著 正確格式如下: socks5://localhost:1080, https://localhost:1080
```

## Build

```
pipenv run pyinstaller -F -n rrbot.exe --add-binary "chromedriver.exe;." main.py
```

### 第一次使用

```
# Use python
$ pipenv run python main.py -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash -f
$ pipenv run python main.py -l FB -p FB_ACCOUNT -u RRCash -f
```

用 rrbot.exe 可取代 pipenv run python main.py
ex:

```
./rrbot.exe -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash -f
./rrbot.exe -l FB -p FB_ACCOUNT -u RRCash -f
```

### 你買不起高帳

```
$ pipenv run python main.py -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash -f --poor
```

### Use proxy

```
pipenv run python main.py -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash --proxy socks5://localhost:1080
```
