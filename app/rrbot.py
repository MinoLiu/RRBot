import os, time
from random import randint
from bs4 import BeautifulSoup

from app import LOG
from app.upgrade import Perk
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RRBot:
    """
    A RRBot class.

    : param login_method: str            GOOGLE,FB,VK
    : param use_to_upgrade: str          RRCash, GOLD
    : param upgrade_perk: str or None    None: Follow my recommend or "STR", "EDU", "END"
    : param profile: str                 Anything, use to save profile
    : param first_login: bool            True to wait 60 seconds for first login, else False
    """
    def __init__(self,
                 login_method="GOOGLE",
                 use_to_upgrade="RRCash",
                 profile="default",
                 upgrade_perk=None,
                 first_login=False,
                 proxy=None,
                 headless=None):
        self.uri = {
            'host': "https://rivalregions.com",
            'overview': "https://rivalregions.com/#overview",
            'work': "https://rivalregions.com/#work",
            'war': "https://rivalregions.com/#war"
        }

        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        options.add_argument("user-data-dir={}".format(
            os.path.join(os.path.abspath(os.getcwd()),
                         'chromeData_' + profile)))
        if proxy:
            options.add_argument('--proxy-server={}'.format(proxy))

        self.driver = webdriver.Chrome(chrome_options=options)
        self.login_method = login_method
        
        self.use_to_upgrade = use_to_upgrade
        if upgrade_perk == "STR":
            self.upgrade_perk = Perk.STR
        elif upgrade_perk == "EDU":
            self.upgrade_perk = Perk.EDU
        elif upgrade_perk == "END":
            self.upgrade_perk = Perk.END
        else:
            self.upgrade_perk = None

        self.first_login = first_login
        self.perks = {}
        self.login()
        self.sleep(5)

    def start(self):
        while (True):
            self.idle()
            self.sleep()

    def refresh(self):
        self.driver.refresh()

    def close(self):
        self.driver.close()

    def check_login(self):
        self.driver.implicitly_wait(10)
        self.sleep(10)
        try:
            self.driver.execute_script('return c_html')
        except JavascriptException as err:
            LOG.debug(err.msg)
            self.login()

    def sleep(self, sec=randint(10, 30)):
        if (sec >= 120):
            LOG.info("Wait for {:.1f} minutes".format(sec / 60.0))
        time.sleep(sec)

    def login(self):
        self.driver.get(self.uri['host'])
        self.driver.implicitly_wait(10)
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

    def upgrade(self, perk):
        xpath = None
        upgrade_xpath = '//*[@id="perk_target_4"]/div[1]/div[1]/div' if self.use_to_upgrade != "GOLD" else '//*[@id="perk_target_4"]/div[2]/div[1]/div'
        button = None
        try:
            if perk == Perk.STR:
                xpath = '//*[@id="index_perks_list"]/div[4]'
            elif perk == Perk.EDU:
                xpath = '//*[@id="index_perks_list"]/div[5]'
            elif perk == Perk.END:
                xpath = '//*[@id="index_perks_list"]/div[6]'
            button = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException as err:
            LOG.debug(err.msg)

        action = ActionChains(self.driver)
        action.move_to_element(button).click(button).perform()
        subaction = wait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, upgrade_xpath)))
        subaction.click()
        LOG.info("Upgrading {}: {} -> {}".format(perk.name,
                                                 self.perks[perk.name],
                                                 self.perks[perk.name] + 1))
        self.sleep(5)

    def calculate_perk_time(self):
        self.driver.get(self.uri['overview'])
        self.driver.implicitly_wait(10)
        self.refresh()
        self.sleep(5)
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
        if counter := soup.find("div", {"id": "perk_counter_2"}):
            t = counter.text
            if (len(t) == 8):  #format: 00:00:00
                return 3600 * int(t[0:2:1]) + 60 * int(t[3:5:1]) + int(t[6:8:1])
            elif (len(t) == 5):  #format: 00:00
                return 60 * int(t[0:2:1]) + int(t[3:5:1])
        return 0

    def idle(self):
        self.refresh()
        self.check_login()
        if self.calculate_perk_time() == 0:
            if self.upgrade_perk is not None:
                self.upgrade(self.upgrade_perk)
            else:
                perk = Perk.perk_strategy(**self.perks)
                self.upgrade(perk)

        if time := self.calculate_perk_time():
                self.sleep(time)
