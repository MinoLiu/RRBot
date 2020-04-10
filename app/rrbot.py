import os, time
from random import randint
from bs4 import BeautifulSoup

from app import LOG
from app import utils
from app.utils import Perk
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
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
                 headless=None,
                 poor=None
                 ):

        self.uri = {
            'host': "https://rivalregions.com",
            'overview': "https://rivalregions.com/#overview"
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
        self.driver.implicitly_wait(10)

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
        self.driver.get(self.uri['host'])
        self.check_login()

    def start(self):
        LOG.info('Bot start')
        while (True):
            self.idle()
            self.sleep()


    def move_and_click(self, by, what, delay=3, wait=10):
        """

        : param by: (By)     By.ID、By.XPATH ...
        : param what: (str)  id、xpath ...
        : param delay: (int)
        ex:
            self.move_and_click(By.ID, "OOF")
        """
        WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((by, what)))
        button = self.driver.find_element(by, what)
        action = ActionChains(self.driver)
        action.move_to_element(button).click(button).perform()
        self.sleep(delay)


    def refresh(self):
        self.driver.refresh()

    def quit(self):
        self.driver.quit()

    def check_login(self):
        self.sleep(10)
        try:
            self.driver.execute_script('return c_html')
        except JavascriptException as err:
            self.login()

    def sleep(self, sec=randint(10, 30)):
        if (sec >= 120):
            LOG.info("Wait for {:.1f} minutes".format(sec / 60.0))
        time.sleep(sec)

    def login(self):
        self.driver.get(self.uri['host'])
        button = None
        xpath = None
        if self.login_method == "FB":
            xpath = '//*[@id="sa_add2"]/div[2]/a[1]/div'
        elif self.login_method == "VK":
            xpath = '//*[@id="sa_add2"]/div[2]/a[3]/div'
        else:
            xpath = '//*[@id="sa_add2"]/div[2]/a[2]/div'
            
        self.move_and_click(By.XPATH, xpath)
        LOG.info("click login button")
        if self.first_login:
            self.sleep(60)
            self.first_login = False

        self.check_login()

    def upgrade(self, perk):
        xpath = None
        upgrade_xpath = '//*[@id="perk_target_4"]/div[1]/div[1]/div' if self.use_to_upgrade != "GOLD" else '//*[@id="perk_target_4"]/div[2]/div[1]/div'
        if perk == Perk.STR:
            xpath = '//*[@id="index_perks_list"]/div[4]'
        elif perk == Perk.EDU:
            xpath = '//*[@id="index_perks_list"]/div[5]'
        elif perk == Perk.END:
            xpath = '//*[@id="index_perks_list"]/div[6]'

        self.move_and_click(By.XPATH, xpath)
        self.move_and_click(By.XPATH, upgrade_xpath)

        LOG.info("Upgrading {}: {} -> {}".format(perk.name,
                                                 self.perks[perk.name],
                                                 self.perks[perk.name] + 1))
        self.sleep(5)

    def calculate_perk_time(self):
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
        if countdown := soup.find("div", {"id": "perk_counter_2"}):
            return utils.convert_str_time(countdown.text)

        return 0

    def idle(self):
        self.refresh()
        self.check_login()

        self.driver.get(self.uri['overview'])
        self.refresh()
        self.sleep(5)
        if self.calculate_perk_time() == 0:
            if self.upgrade_perk is not None:
                self.upgrade(self.upgrade_perk)
            else:
                perk = Perk.perk_strategy(**self.perks)
                self.upgrade(perk)

        self.driver.get(self.uri['overview'])
        self.refresh()
        self.sleep(5)
        if time := self.calculate_perk_time():
                self.sleep(time)



class PoorBot(RRBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def check_gold(self):
        """
        Must be work page
        """
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
        gold = float(soup.find("span", {"class":"imp yellow tip"}).text)

        return gold

    def check_energy(self):
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
        energy = int(soup.find("span", {"id":"s"}).text)
        sec = 0

        if countdown := soup.find("span", {"id":"header_my_fill_bar_countdown"}):
            sec = utils.convert_str_time(countdown.text)

        return energy, sec

    def check_perk(self):
        self.move_and_click(By.XPATH, "//div[@action='main/content']", 5)
        if self.calculate_perk_time() == 0:
            if self.upgrade_perk is not None:
                self.upgrade(self.upgrade_perk)
            else:
                perk = Perk.perk_strategy(**self.perks)
                self.upgrade(perk)

    def check_travel(self):
        self.move_and_click(By.XPATH, "//div[@action='main/content']", 5)
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
        if soup.find("div", {"class":"button_red pointer map_d_b_ind index_registartion_home"}):
            return True
        return False

    def check_war(self):
        self.move_and_click(By.XPATH, "//div[@action='main/content']", 5)
        soup = BeautifulSoup(self.driver.page_source, "html5lib")
        if countdown := soup.find("span", {"class": "small tip dot pointer war_index_war_countdown hasCountdown"}):
            if (t := utils.convert_str_time(countdown.text)) > 0:
                return t
        
        self.move_and_click(By.XPATH, "//div[@action='war']")
        self.move_and_click(By.CLASS_NAME, "war_4_start")
        self.move_and_click(By.CLASS_NAME, "war_w_send_ok")
        self.move_and_click(By.ID, "slide_close")
        

    def mining(self):
        self.move_and_click(By.XPATH, "//div[@action='work']")

        energy, sec = self.check_energy()
        gold = self.check_gold()

        soup = BeautifulSoup(self.driver.page_source, "html5lib")
        if soup.find("div", {"class": "work_factory_button button_blue"}) is None:
            LOG.info("Working is not possible")
            return 600

        if gold > 0 and energy >= 10:
            self.move_and_click(By.XPATH, "//div[@class='work_factory_button button_blue']", 5)
            self.move_and_click(By.ID, "slide_close")
        elif gold > 0 and sec == 0:
            self.move_and_click(By.ID, "header_my_fill_bar")
        else:
            if gold == 0 or energy >= 10 or sec == 0:
                LOG.info("Lack of gold or other problems")
            return sec

        return self.mining()


    def idle(self):
        sec = 0
        if not self.check_travel():
            self.check_war()
            sec = self.mining()

        self.check_perk()
        if sec == 0:
            self.sleep(600)
        else:
            self.sleep(sec)