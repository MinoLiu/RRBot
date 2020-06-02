from enum import Enum
from bs4 import BeautifulSoup


class aobject(object):
    """
    Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """

    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass


class Status:

    @staticmethod
    def energy_bar_selector() -> str:
        return "#header_my_fill_bar"

    @staticmethod
    def check_energy(soup: BeautifulSoup) -> (int, int):
        energy = int(soup.find("span", {"id": "s"}).text)
        sec = 0
        countdown = soup.find("span", {"id": "header_my_fill_bar_countdown"})
        if countdown:
            sec = convert_str_time(countdown.text)

        return energy, sec

    @staticmethod
    def check_money(soup) -> (int, int):
        gold = int(soup.find("span", {"id": "g"}).text.replace('.', ''))
        money = int(soup.find("span", {"id": "m"}).text.replace('.', ''))
        return gold, money

    @staticmethod
    def check_str_money(soup) -> (str, str):
        return (soup.find("span", {"id": "g"}).text, soup.find("span", {"id": "m"}).text)


class Overview:
    url = "https://rivalregions.com/#overview"

    @staticmethod
    def selector() -> str:
        return "div.item_menu[action='main/content']"

    @staticmethod
    def check_war(soup: BeautifulSoup) -> int:
        countdown = soup.find("span", {"class": "small tip dot pointer war_index_war_countdown hasCountdown"})
        if countdown:
            return convert_str_time(countdown.text)
        return 0

    @staticmethod
    def check_travel(soup: BeautifulSoup) -> bool:
        if soup.find("div", {"class": "button_red pointer map_d_b_ind index_registartion_home"}):
            return True
        return False


class Work:

    @staticmethod
    def selector() -> str:
        return "div[action='work']"

    @staticmethod
    def work_selector() -> str:
        return ".work_factory_button.button_blue"

    @staticmethod
    def check_region_gold(soup: BeautifulSoup) -> float:
        return float(soup.find("span", {"class": "imp yellow tip"}).text)

    @staticmethod
    def can_work(soup: BeautifulSoup):
        if soup.find("div", {"class": "work_factory_button button_blue"}) is None:
            return False
        return True


class Storage(Enum):
    Aircrafts = 1
    Tanks = 2
    Oil = 3
    Ore = 4
    Uranium = 11
    Diamonds = 15
    Liquidoxygen = 21
    Helium3 = 24
    Rivalium = 26
    Antirad = 13
    Energydrink = 17
    Spacerockets = 20
    LSS = 25
    Missiles = 14
    Bombers = 16
    Battleships = 18
    Laserdrones = 27
    Moontanks = 22
    Spacestations = 23

    @classmethod
    def selector(cls, storage_id=None):
        if storage_id is None:
            return "div[action='storage']"

        if cls.has_value(storage_id):
            return ".storage_item[url='{}']".format(storage_id)

        raise Exception("Storage_id {} not exist in StorageEnum".format(storage_id))

    @classmethod
    def has_value(cls, storage_id):
        return storage_id in cls._value2member_map_

    @staticmethod
    def check_product_price(soup: BeautifulSoup) -> (int, int):
        max_num = int(
            soup.find("span", {
                "class": "dot hov2 pointer small storage_market_number"
            }).text.replace('.', '')
        )
        price = int(
            soup.find("div", {
                "class": "float_left storage_price small"
            }).find("span", {
                "class": "dot"
            }).text.replace('.', '').replace(' $', '')
        )
        return price, max_num


class War:
    url = "https://rivalregions.com/#war"

    @staticmethod
    def selector():
        return "div[action='war']"

    @staticmethod
    def military_training_selector():
        return ".war_4_start"

    @staticmethod
    def bombers_selector():
        return ".war_w_unit > span[url='16']"

    @staticmethod
    def auto_once_per_hour_selector():
        return ".war_w_auto_wd"

    @staticmethod
    def send_ok_selector():
        return ".war_w_send_ok"


class Perks(Enum):
    STR = 0
    EDU = 1
    END = 2

    @staticmethod
    def perk_strategy(STR, EDU, END, strategy=[2, 1, 1]):
        """
        Used to decide which one to upgrade
        : param STR tuple(int: point, int: sec)
        : param EDU tuple(int: point, int: sec)
        : param END tuple(int: point, int: sec)
        : param strategy list(int)
        """
        perk = None
        if END[0] < 50:
            perk = Perks.END
        elif STR[0] < 50:
            perk = Perks.STR
        elif EDU[0] < 50:
            perk = Perks.EDU
        elif END[0] < 100:
            perk = Perks.END
        elif STR[0] < 100:
            perk = Perks.STR
        elif EDU[0] < 100:
            perk = Perks.EDU
        else:
            if float(STR[1]) / END[1] > (float(strategy[0]) / strategy[2]):
                perk = Perks.END
            elif float(STR[1]) / EDU[1] > (float(strategy[0]) / strategy[1]):
                perk = Perks.EDU
            else:
                perk = Perks.STR
        return perk if perk is not None else Perks.STR


def convert_str_time(t: str):
    """
    : t: (str)    Format: 00:00:00 or 00:00 or '1 d 00:00:00'
    """
    t = t.strip()
    if (len(t) == 8):
        return 3600 * int(t[0:2:1]) + 60 * int(t[3:5:1]) + int(t[6:8:1])
    elif (len(t) == 5):
        return 60 * int(t[0:2:1]) + int(t[3:5:1])
    elif (len(t.split(' ')) >= 3):
        day, _, _t = t.split(' ')

        return int(day) * 3600 * 24 + convert_str_time(_t)

    raise AttributeError("'{}', Format Error".format(t))


def close_selector() -> str:
    return "#slide_close"
