import base64
import json
import os

from src.core import Singleton


class AppSetting(metaclass=Singleton):
    """
    Setting of App level
    Initializes when the app startup
    """
    APP_NAME: str = "Stem"
    APP_VERSION: str = "1.0.0"
    APP_VERSION_PATH: str = "/api"
    DEBUG = bool(os.getenv("APP_MODE") == "debug")
    PORT = int(os.getenv("PORT") or 9000)
    SECURITY_KEY: str = os.getenv("SECURITY_KEY") or "tests"

    PG_CONF: dict
    REDIS_CONF: dict

    def __init__(self):
        app_setting_str = os.getenv("APP_SETTINGS") or 'e30='

        app_setting: dict = json.loads(base64.b64decode(
            app_setting_str.encode()).decode())
        self.REDIS_CONF: dict = app_setting.get("redis_conf")
        self.PG_CONF: dict = app_setting.get("pg_conf")

        app_conf = app_setting.get("app_conf")
        self.DEBUG = app_conf.get("APP_MODE") == "debug"
        self.SECURITY_KEY = app_conf.get("SECURITY_KEY")
