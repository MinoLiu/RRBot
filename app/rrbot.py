import pickle
from random import randint
from bs4 import BeautifulSoup

from app import LOG
from app import utils
from app.utils import Perks, Storage, Overview, Status
from app.browser import Browser
import asyncio


class RRBot(utils.aobject):
    """
    A RRBot class.
    """

    async def __init__(
        self,
        login_method="GOOGLE",
        use_to_upgrade="RRCash",
        profile="default",
        upgrade_perk=None,
        upgrade_strategy="2:1:1",
        proxy=None,
        headless=None,
        poor=None
    ):
        self.profile = profile

        self.uri = "https://rivalregions.com"
        self.headless = headless
        if proxy:
            proxy = "--proxy-server={}".format(proxy)

        self.browser = await Browser(headless, proxy)
        self.browser.set_default_navigation_timeout(30000)

        self.login_method = login_method
        self.use_to_upgrade = use_to_upgrade
        try:
            self.upgrade_strategy = [int(x) for x in upgrade_strategy.split(':')]
            assert len(self.upgrade_strategy) == 3
        except Exception:
            LOG.error("--upgrade_strategy invalid")

        self.perks = {'strategy': self.upgrade_strategy}

        if upgrade_perk == "STR":
            self.upgrade_perk = Perks.STR
        elif upgrade_perk == "EDU":
            self.upgrade_perk = Perks.EDU
        elif upgrade_perk == "END":
            self.upgrade_perk = Perks.END
        else:
            self.upgrade_perk = None

        await self.load_cookies()

        await self.browser.goto(self.uri, waitUntil='networkidle0')
        await self.check_login()

    async def save_cookies(self):
        cookies = await self.browser.cookies(
            'https://rivalregions.com/', 'https://www.facebook.com/', 'https://accounts.google.com/',
            'https://oauth.vk.com/'
        )

        pickle.dump(cookies, open("{}.pkl".format(self.profile), "wb"))
        LOG.info("Cookies saved!")

    async def load_cookies(self):
        try:
            cookies = pickle.load(open("{}.pkl".format(self.profile), "rb"))
            for cookie in cookies:
                await self.browser.set_cookie(cookie)
            LOG.info("Cookies loaded!")
        except Exception:
            LOG.info('First Login')
            if self.headless:
                LOG.error('Please do not use headless mode!')

    async def start(self):
        LOG.info('Bot start')
        while (True):
            await self.idle()
            await self.sleep(5)

    async def idle(self):
        await self.refresh()
        await self.check_login()

        await self.do_perks_upgrade()
        await self.do_storage_supply()

        _, _, (energy, energy_cooldown_time) = await self.check_overview()

        if (energy >= 20) and energy_cooldown_time == 0:
            LOG.warn("There is no gold in your area or automatic working expires")

        time = await self.calculate_perks_time()
        if time:
            await self.sleep(21600 if time >= 21600 else time)

    async def click(self, selector: str, wait_for=None, wait_for_navigation=False, wait_for_sec=30):
        await self.browser.wait_for(selector, timeout=wait_for_sec * 1000)

        # IDK why it doesn't work
        #       await self.browser.click(selector)

        if wait_for_navigation:
            asyncio.wait([
                self.browser.query_selector_eval(selector, 'el => el.click()'),
                self.browser.wait_for_navigation(waitUntil='networkidle0')
            ])
        else:
            # Use js instead
            await self.browser.query_selector_eval(selector, 'el => el.click()')

        if wait_for:
            await self.browser.wait_for(wait_for, timeout=wait_for_sec * 1000)

        await self.sleep(1)

    async def type(self, selector: str, text: str, delay: int = 0):
        await self.browser.clear(selector)
        await self.browser.type(selector, text, delay=delay)

    async def refresh(self):
        await self.browser.reload(waitUntil='networkidle0')

    async def close(self):
        await self.browser.close()

    async def quit(self):
        await self.browser.quit()

    async def sleep(self, sec=randint(10, 30)):
        if (sec >= 120):
            LOG.info("Wait for {:.1f} minutes".format(sec / 60.0))
        await asyncio.sleep(sec)

    async def get_soup(self):
        return BeautifulSoup(await self.browser.content(), "html5lib")

    async def check_login(self):
        try:
            await self.browser.wait_for('() => {return c_html;}', timeout=10000)
        except Exception as err:
            LOG.debug(err)
            await self.login()

    async def login(self):
        await self.browser.goto(self.uri, waitUntil='networkidle0')
        selectors = {
            'FB': '.sa_link[href*="facebook.com"]',
            'GOOGLE': '.sa_link[href*="google.com"]',
            'VK': '.sa_link[href*="vk.com"]'
        }
        try:
            await self.browser.click(selectors[self.login_method]),
            await self.browser.wait_for_response('https://rivalregions.com/', timeout=240000)
            await self.browser.wait_for('#chat input[name=name]', timeout=10000)
            name = await self.browser.query_selector_eval('#chat input[name=name]', 'node => node.value')
            LOG.info("Login success {}".format(name))
            await self.save_cookies()
        except Exception as err:
            LOG.info(err)

        await self.check_login()

    async def upgrade(self, perk):
        selector = None
        upgrade_selector = "#perk_target_4 > div[url='{}'] > div > div".format(
            2 if self.use_to_upgrade == "GOLD" else 1
        )
        if perk == Perks.STR:
            selector = ".perk_item[perk='1']"
        elif perk == Perks.EDU:
            selector = ".perk_item[perk='2']"
        elif perk == Perks.END:
            selector = ".perk_item[perk='3']"
        else:
            raise Exception("Perk not found")

        await self.click(selector, wait_for=upgrade_selector)
        await self.click(upgrade_selector)
        await self.sleep(3)

        LOG.info("Upgrading {}: {} -> {}".format(perk.name, self.perks[perk.name][0], self.perks[perk.name][0] + 1))

    async def calculate_perks_time(self) -> int:
        soup = await self.get_soup()

        countdown = soup.find("div", {"id": "perk_counter_2"})
        if countdown:
            return utils.convert_str_time(countdown.text)

        time_texts = soup.find_all("div", {"class": "perk_4"})
        self.perks['STR'] = (
            int(soup.find("div", {
                "perk": "1",
                "class": "perk_source_2"
            }).text), utils.convert_str_time(time_texts[0].text.strip().split("$, ")[-1])
        )
        self.perks['EDU'] = (
            int(soup.find("div", {
                "perk": "2",
                "class": "perk_source_2"
            }).text), utils.convert_str_time(time_texts[2].text.strip().split("$, ")[-1])
        )
        self.perks['END'] = (
            int(soup.find("div", {
                "perk": "3",
                "class": "perk_source_2"
            }).text), utils.convert_str_time(time_texts[4].text.strip().split("$, ")[-1])
        )

        return 0

    async def buy_product(self, storage_id, amount):
        """
        Must be #storage page

        : Storage_id (Storage):   Storage.Bombers、.....
        : amount (int)
        """
        await self.click(Storage.selector(storage_id.value))
        await self.sleep(3)
        price, num = Storage.check_product_price(await self.get_soup())
        _, money = Status.check_money(await self.get_soup())
        # Reserve 5 milion for upgrade
        money -= 5000000

        if money < price:
            return

        amount = amount if num >= amount else num
        if price * amount > money:
            amount = money // price

        await self.type('.storage_buy_input', str(amount))
        await self.click('.storage_buy_button')
        await self.sleep(3)
        LOG.info("Market purchase: {}, {} pcs, total {}.".format(storage_id.name, amount, price * amount))

    async def do_storage_supply(self):
        await self.click(Storage.selector(), wait_for=".storage_number")
        soup = BeautifulSoup((await self.browser.content()), "html5lib")

        # Produce energy drink
        if int(soup.find("span", {"urlbar": str(Storage.Energydrink.value)}).text.replace('.', '')) <= 10800:
            await self.click(Storage.selector(Storage.Energydrink.value))
            await self.sleep(3)
            gold, _ = Status.check_money(await self.get_soup())

            # 6 hours
            amount = 10800
            if gold < 1080:
                amount = gold * 10

            await self.type('.storage_produce_ammount', str(amount))
            await self.click('.storage_produce_button')
            await self.sleep(3)
            LOG.info('Produced: energy drink {} pcs.'.format(amount))

        # Buy Bombers
        if int(soup.find("span", {"urlbar": str(Storage.Bombers.value)}).text.replace('.', '')) < 10000:
            await self.buy_product(Storage.Bombers, 10000)

        # Buy Moon tanks
        if int(soup.find("span", {"urlbar": str(Storage.Moontanks.value)}).text.replace('.', '')) < 10000:
            await self.buy_product(Storage.Moontanks, 10000)

    async def do_perks_upgrade(self) -> int:
        await self.click(Overview.selector(), wait_for='#chat input[name=name]')
        t = await self.calculate_perks_time()
        if t == 0:
            if self.upgrade_perk is not None:
                await self.upgrade(self.upgrade_perk)
            else:
                perk = Perks.perk_strategy(**self.perks)
                await self.upgrade(perk)
            return 600
        else:
            return t

    async def check_overview(self) -> (int, bool, (int, int)):
        """
        Return
            (
                wars_cooldown_time,
                is_traveling,
                (energy, energy_cooldown_time)
            )
        """
        await self.click(Overview.selector(), wait_for='#chat input[name=name]')
        soup = await self.get_soup()
        return (Overview.check_war(soup), Overview.check_travel(soup), Status.check_energy(soup))
