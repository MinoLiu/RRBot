import argparse
import logging
from logging import handlers
import asyncio
import os
import signal
import psutil


def kill_child_processes(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)

    for process in children:
        process.send_signal(sig)


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


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--login_method", help="登入選項: 'GOOGLE'、'FB'、'VK'", dest='login_method')
    parser.add_argument(
        "-u", "--use_to_upgrade", help="升級道具: 'RRCash'、'GOLD' 預設使用 RRCash", default='RRCash', dest='use_to_upgrade'
    )
    parser.add_argument("-p", "--profile", help="帳戶profile: 預設為'default', 修改可更換帳戶", default='default', dest='profile')

    parser.add_argument(
        "--upgrade_perk", help="只升級指定的選項 'STR'、'EDU'、'END' 不指定將會使用upgrade_strategy", dest='upgrade_perk'
    )

    parser.add_argument("--poor", help="你是窮人, 你買不起高級會員, 你必須手動挖礦、軍演, 可憐哪 我來幫你", action="store_true")

    parser.add_argument("--headless", help="確定使用者有登入成功後可開啟 將瀏覽器GUI關閉節省資源", action="store_true", dest='headless')

    parser.add_argument("--proxy", help="正確格式如下: socks5://localhost:1080, https://localhost:1080", dest='proxy')

    parser.add_argument(
        "--upgrade_strategy", help="三圍100後將按照時間比例來升級 default '2:1:1'", default='2:1:1', dest="upgrade_strategy"
    )

    args = parser.parse_args()
    if (args.login_method is None):
        parser.print_help()
    else:
        initLog(args.profile)
        from app import LOG

        while (True):
            r = None
            if args.poor is True:
                from app.poorbot import PoorBot
                r = await PoorBot(**vars(args))
            else:
                from app.rrbot import RRBot
                r = await RRBot(**vars(args))
            try:
                await r.start()
                break
            except Exception as err:
                LOG.error('Bot detect error: {}'.format(err))
                # Due to "browser.close" sometime not working, use kill child processes instead.
                kill_child_processes(os.getpid())
                # await r.quit()
                LOG.info('Restarting...')


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
