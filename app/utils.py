from enum import Enum


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
    def xpath(cls, storage_id):
        if cls.has_value(storage_id):
            return "//span[@urlbar='{}']".format(storage_id)

        raise Exception("Storage_id {} not exist in StorageEnum".format(storage_id))

    @classmethod
    def has_value(cls, storage_id):
        return storage_id in cls._value2member_map_


class Perk(Enum):
    STR = 0
    EDU = 1
    END = 2

    @staticmethod
    def perk_strategy(STR, EDU, END):
        """
        Used to decide which one to upgrade
        : param STR: tuple(int: point, int: sec)
        : param EDU: tuple(int: point, int: sec)
        : param END: tuple(int: point, int: sec)
        """
        perk = None
        if END[0] < 50:
            perk = Perk.END
        elif STR[0] < 50:
            perk = Perk.STR
        elif EDU[0] < 50:
            perk = Perk.EDU
        elif END[0] < 100:
            perk = Perk.END
        elif STR[0] < 100:
            perk = Perk.STR
        elif EDU[0] < 100:
            perk = Perk.EDU
        else:
            if float(STR[1]) / END[1] > 2.0:
                perk = Perk.END
            elif float(STR[1]) / EDU[1] > 1.0:
                perk = Perk.EDU
            else:
                perk = Perk.STR
        return perk if perk is not None else Perk.STR


def convert_str_time(t):
    """
    : t: (str)    Format: 00:00:00 or 00:00
    """
    t = t.strip()
    if (len(t) == 8):
        return 3600 * int(t[0:2:1]) + 60 * int(t[3:5:1]) + int(t[6:8:1])
    elif (len(t) == 5):
        return 60 * int(t[0:2:1]) + int(t[3:5:1])

    raise AttributeError("'{}', Format Error".format(t))
