from typing import Union


def round_num(num: Union[float, str, None], precision: int = 2):
    if not num:
        return 0
    return round(float(num), precision)


def _round(num: float, decimal_places: int = 2) -> float:
    """ Only keep the 2 decimal places. """
    num = num or 0
    num = float(num)
    scale = 10 ** decimal_places
    return round(num * scale) / scale


def price_round(price: float, decimal_places: int = 2) -> float:
    """ Only keep the 2 decimal places. """
    return round_num(price, decimal_places)
