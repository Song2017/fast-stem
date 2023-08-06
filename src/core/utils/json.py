__all__ = [
    "json_dumps_unicode",
    "json_loads",
    "camel_string",
    "underscore_string",
    "filter_none_list"
]

import json
import re
from typing import Union


def json_dumps_unicode(obj):
    """
    Change Python default json.dumps acting like JavaScript, including allow
    Chinese characters and no space between any keys or values.
    """
    return json.dumps(obj,
                      ensure_ascii=False,
                      separators=(',', ':'),
                      cls=RawDataEncoder
                      )


class RawDataEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, bytes):
            return o.decode("utf-8")
        return super(RawDataEncoder, self).default(o)


def json_loads(json_str: str) -> Union[dict, str]:
    """ An enhanced version of json.loads. """
    try:
        return json.loads(json_str)
    except Exception as e:
        print(f"""Error json_loads: {e}""")
        return json_str


def underscore_string(word: str) -> str:
    """
    Make an underscored, lowercase form from the expression in the string.

    Example::

        >>> underscore_string("DeviceType")
        'device_type'

    As a rule of thumb you can think of :func:`underscore` as the inverse of
    :func:`camelize`, though there are cases where that does not hold::
    """
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def camel_string(input_str: str, uppercase_first_letter: bool = True) -> str:
    """
    Convert strings to CamelCase.

    Examples::

        >>> camel_string("device_type")
        'DeviceType'
        >>> camel_string("device_type", False)
        'deviceType'

    :func:`camelize` can be thought of as a inverse of :func:`underscore`,
    although there are some cases where that does not hold::

        >>> camel_string(underscore_string("IOError"))
        'IoError'
    :param input_str
    :param uppercase_first_letter: if set to `True` :func:`camelize` converts
        strings to UpperCamelCase. If set to `False` :func:`camelize` produces
        lowerCamelCase. Defaults to `True`.
    """
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(),
                      input_str)
    else:
        return input_str[0].lower() + camel_string(input_str)[1:]


def filter_none_list(data_list: list) -> list:
    """
    Remove none or empty items in list object
    """
    if not isinstance(data_list, list):
        return []
    return [o for o in data_list if o]
