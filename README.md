# RRBot

A bot for RR

- [x] Perk upgrading
- [ ] Working
- [ ] Military training
- [ ] Weapon replenishment and energy drinks

## Install

```
$ pipenv install
```

## Usage:

```
$ pipenv run python main.py
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
  --headless            預設為False, True將會停用瀏覽器GUI (由於headless chrome目前有bug無法共通user-data所以目前無法使用)
  --proxy PROXY         請先去確認proxy活著 正確格式如下: socks5://localhost:1080, https://localhost:1080
```

```
$ pipenv run python main.py -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash -f
$ pipenv run python main.py -l FB -p FB_ACCOUNT -u RRCash -f
```

Use proxy

```
pipenv run python main.py -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash --proxy socks5://localhost:1080
```
