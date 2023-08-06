import arrow
from arrow import parser

__all__ = [
    "CHINA_TIMEZONE",
    "CHINESE_TIME_FORMAT",
    "ISO8601_TIME_FORMAT",
    "ZZ_TIME_FORMAT",

    "fix_with_timezone",
    "format_timestamp",
    "format_timestamp_day",

    "SECOND",
    "MINUTE",
    "HOUR",
    "DAY",
    "WEEK",
]

"""
Note: Switch to use arrow instead of maya, due to maya requires c_extension,
and can't run on Alibaba Function Compute
"""

CHINA_TIMEZONE = "Asia/Shanghai"
CHINESE_TIME_FORMAT = "YYYY-MM-DD HH:mm:ss"
ISO8601_TIME_FORMAT = "YYYY-MM-DDTHH:mm:ss"
ZZ_TIME_FORMAT = "YYYY-MM-DDTHH:mm:ssZZ"
ISO_DATE_FORMAT = "ISO8601"

SECOND = 1
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7


def fix_with_timezone(
        time: str,
        zone=CHINA_TIMEZONE,
        target_format=CHINESE_TIME_FORMAT
) -> str:
    """ Fill the missing zone information. """
    if not time:
        return time
    to_zone = parser.TzinfoParser.parse(zone)
    # Zone information
    if "+" in time:
        aa = arrow.get(time)
    elif "z" in time.lower():
        aa = arrow.get(time).to(to_zone)
    else:
        aa = arrow.get(arrow.get(time).datetime, to_zone)

    if target_format == ISO_DATE_FORMAT:
        return aa.isoformat()
    else:
        return aa.format(target_format)


def format_timestamp(t: str) -> str:
    return fix_with_timezone(t, target_format="YYYYMMDDhhmmss")


def format_timestamp_day(t: str) -> str:
    return fix_with_timezone(t, target_format="YYYYMMDD")
