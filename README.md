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
$ python main.py
usage: main.py [-h] [-l LOGIN_METHOD] [-u USE_TO_UPGRADE] [-p PROFILE] [-j JUST_UPGRADE] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -l LOGIN_METHOD, --login_method LOGIN_METHOD
                        登入選項: 'GOOGLE'、'FB'、'VK'
  -u USE_TO_UPGRADE, --use_to_upgrade USE_TO_UPGRADE
                        升級道具: 'RRCash'、'GOLD' 預設使用 RRCash
  -p PROFILE, --profile PROFILE
                        帳戶profile: 預設為'default', 修改可更換帳戶
  -j JUST_UPGRADE, --just_upgrade JUST_UPGRADE
                        生級指定選項 'STR'、'EDU'、'END' 不指定將會使用Discord社群推薦的配點
  -f, --first_login     預設為False, True將會等待60秒讓使用者登入
```

```
$ python main.py -l GOOGLE -p GOOGLE_ACCOUNT -u RRCash -f
$ python main.py -l FB -p FB_ACCOUNT -u RRCash -f
```
