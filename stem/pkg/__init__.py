import os

from stem.pkg.conf import AppSetting

UTF8 = "utf-8"
PROJECT_DIR = os.path.dirname(__file__).replace("/stem", "").replace(
    r"\\stem", "").replace("/pkg", "").replace(r"\\pkg", "")

APP_CONF = AppSetting()

__all__ = [
    "UTF8",
    "PROJECT_DIR",

    "AppSetting",
    "APP_CONF",
]
