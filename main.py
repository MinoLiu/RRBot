import argparse
import logging
from logging import handlers


def initLog(profile):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[
            logging.StreamHandler(),
            handlers.RotatingFileHandler('{}.log'.format(profile), "w", 1024 * 1024 * 100, 3, "utf-8")
        ]
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--login_method", help="登入選項: 'GOOGLE'、'FB'、'VK'", dest='login_method')
    parser.add_argument(
        "-u", "--use_to_upgrade", help="升級道具: 'RRCash'、'GOLD' 預設使用 RRCash", default='RRCash', dest='use_to_upgrade'
    )
    parser.add_argument("-p", "--profile", help="帳戶profile: 預設為'default', 修改可更換帳戶", default='default', dest='profile')

    parser.add_argument("--upgrade_perk", help="生級指定選項 'STR'、'EDU'、'END' 不指定將會使用Discord社群推薦的配點", dest='upgrade_perk')

    parser.add_argument(
        "-f", "--first_login", help="預設為False, True將會等待60秒讓使用者登入", action="store_true", dest='first_login'
    )

    parser.add_argument("--poor", help="你是窮人, 你買不起高級會員, 你必須手動挖礦、軍演, 可憐哪 我來幫你", action="store_true")

    parser.add_argument(
        "--headless",
        help="預設為False, True將會停用瀏覽器GUI (由於headless chrome目前有bug無法共通user-data所以目前無法使用)",
        action="store_true",
        dest='headless'
    )

    parser.add_argument(
        "--proxy", help="請先去確認proxy活著 正確格式如下: socks5://localhost:1080, https://localhost:1080", dest='proxy'
    )

    args = parser.parse_args()
    if (args.login_method is None):
        parser.print_help()
    else:
        initLog(args.profile)
        from app import LOG
        from app.rrbot import RRBot, PoorBot

        while (True):
            r = None
            if args.poor is True:
                r = PoorBot(**vars(args))
            else:
                r = RRBot(**vars(args))
            try:
                r.start()
                break
            except Exception as err:
                LOG.error('Bot detect error: {}'.format(err))
                r.quit()
                LOG.info('Restarting...')
