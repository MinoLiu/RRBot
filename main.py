from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException, JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os, time, argparse
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[
                        logging.FileHandler('robot.log', 'w', 'utf-8'),
                        logging.StreamHandler()
                    ])

LOG = logging.getLogger(__name__)


class RRBot:
    """
    A RRBot class.

    : param login_method: str            GOOGLE,FB,VK
    : param use_to_upgrade: str          RRCash, GOLD
    : param just_upgrade: str or None    None: Follow my recommend or "STR", "EDU", "END"
    : param profile: str                 Anything, use to save profile
    : param first_login: bool            True to wait 60 seconds for first login, else False
    """
    def __init__(self,
                 login_method="GOOGLE",
                 use_to_upgrade="RRCash",
                 profile="default",
                 just_upgrade=None,
                 first_login=False):
        self.uri = "https://rivalregions.com"
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir={}".format(
            os.path.join(os.path.abspath(os.getcwd()),
                         'chromeData_' + profile)))

        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()
        self.login_method = login_method
        self.use_to_upgrade = use_to_upgrade
        self.just_upgrade = just_upgrade
        self.first_login = first_login
        self.perks = {}
        self.login()

    def refresh(self):
        self.driver.refresh()
        self.check_login()

    def close(self):
        self.driver.close()

    def check_login(self):
        self.sleep(10)
        try:
            self.driver.execute_script('return c_html')
            LOG.info("login success")
            self.idle()
        except JavascriptException as err:
            LOG.debug(err.msg)
            self.login()

    def sleep(self, sec):
        if (sec >= 120):
            LOG.info("Wait for {:.1f} minutes".format(sec / 60.0))
        time.sleep(sec)

    def login(self):
        self.driver.get(self.uri)
        self.sleep(5)
        button = None
        xpath = None
        try:
            if self.login_method == "FB":
                xpath = '//*[@id="sa_add2"]/div[2]/a[1]/div'
            elif self.login_method == "VK":
                xpath = '//*[@id="sa_add2"]/div[2]/a[3]/div'
            else:
                xpath = '//*[@id="sa_add2"]/div[2]/a[2]/div'

            button = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException as err:
            LOG.debug(err.msg)
        else:
            action = ActionChains(self.driver)
            action.move_to_element(button).perform()
            subaction = wait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            subaction.click()
            LOG.info("click login button")
            if self.first_login:
                self.sleep(60)
                self.first_login = False

        self.check_login()

    def upgrade(self, perk_name):
        xpath = None
        upgrade_xpath = '//*[@id="perk_target_4"]/div[1]/div[1]/div' if self.use_to_upgrade != "GOLD" else '//*[@id="perk_target_4"]/div[2]/div[1]/div'
        button = None
        try:
            if perk_name == "STR":
                xpath = '//*[@id="index_perks_list"]/div[4]'
            elif perk_name == "EDU":
                xpath = '//*[@id="index_perks_list"]/div[5]'
            elif perk_name == "END":
                xpath = '//*[@id="index_perks_list"]/div[6]'
            button1 = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException as err:
            LOG.debug(err.msg)
            self.refresh()
            return

        action = ActionChains(self.driver)
        action.move_to_element(button1).click(button1).perform()
        subaction = wait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, upgrade_xpath)))
        subaction.click()
        LOG.info("Upgrading {}: {} -> {}".format(perk_name,
                                                 self.perks[perk_name],
                                                 self.perks[perk_name] + 1))
        self.sleep(5)
        self.idle()

    def idle(self):
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
        self.perks['STR'] = int(
            soup.find("div", {
                "perk": "1",
                "class": "perk_source_2"
            }).text)
        self.perks['EDU'] = int(
            soup.find("div", {
                "perk": "2",
                "class": "perk_source_2"
            }).text)
        self.perks['END'] = int(
            soup.find("div", {
                "perk": "3",
                "class": "perk_source_2"
            }).text)
        counter = soup.find("div", {"id": "perk_counter_2"})
        try:
            LOG.info('Upgrading time {}'.format(counter.text))
        except AttributeError:
            if self.just_upgrade in ["STR", "EDU", "END"]:
                self.upgrade(self.just_upgrade)
            else:
                self.upgrade_stratge()
        else:
            t = counter.text
            if (len(t) == 8):  #format: 00:00:00
                self.sleep(3600 * int(t[0:2:1]) + 60 * int(t[3:5:1]) +
                           int(t[6:8:1]))
            elif (len(t) == 5):  #format: 00:00
                self.sleep(60 * int(t[0:2:1]) + int(t[3:5:1]))

            self.refresh()

    def upgrade_stratge(self):
        STR = self.perks['STR']
        EDU = self.perks['EDU']
        END = self.perks['END']

        if END < 50:
            self.upgrade('END')
        elif STR < 50:
            self.upgrade('STR')
        elif EDU < 50:
            self.upgrade('EDU')
        elif END < 100:
            self.upgrade('END')
        elif STR < 100:
            self.upgrade('STR')
        elif EDU < 100:
            self.upgrade('EDU')
        else:
            if STR / END > 2.0:
                self.upgrade('END')
            elif STR / EDU > 1.0:
                self.upgrade('EDU')
            else:
                self.upgrade('STR')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l",
                        "--login_method",
                        help="登入選項: 'GOOGLE'、'FB'、'VK'",
                        dest='login_method')
    parser.add_argument("-u",
                        "--use_to_upgrade",
                        help="升級道具: 'RRCash'、'GOLD' 預設使用 RRCash",
                        default='RRCash',
                        dest='use_to_upgrade')
    parser.add_argument("-p",
                        "--profile",
                        help="帳戶profile: 預設為'default', 修改可更換帳戶",
                        default='default',
                        dest='profile')

    parser.add_argument("-j",
                        "--just_upgrade",
                        help="生級指定選項 'STR'、'EDU'、'END' 不指定將會使用Discord社群推薦的配點",
                        dest='just_upgrade')

    parser.add_argument("-f",
                        "--first_login",
                        help="預設為False, True將會等待60秒讓使用者登入",
                        action="store_true",
                        dest='first_login')

    args = parser.parse_args()
    if (args.login_method is None):
        parser.print_help()
    else:
        RRBot(**vars(args))
