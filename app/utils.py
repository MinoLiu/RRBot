from enum import Enum


class Perk(Enum):
    STR = 0
    EDU = 1
    END = 2

    @staticmethod
    def perk_strategy(STR, EDU, END):
        """
        Used to decide which one to upgrade
        : param STR: (int)  STR point
        : param EDU: (int)  EDU point
        : param END: (int)  END point
        """
        perk = None
        if END < 50:
            perk = Perk.END
        elif STR < 50:
            perk = Perk.STR
        elif EDU < 50:
            perk = Perk.EDU
        elif END < 100:
            perk = Perk.END
        elif STR < 100:
            perk = Perk.STR
        elif EDU < 100:
            perk = Perk.EDU
        else:
            if STR / END > 2.0:
                perk = Perk.END
            elif STR / EDU > 1.0:
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