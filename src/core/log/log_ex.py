import logging
import sys
from datetime import datetime
from functools import cached_property
from typing import Any

from src.core.utils.json import json_dumps_unicode


class LogEx:
    """Logging configuration to be set for the server"""

    def __init__(self, **data: Any):
        # e.g. youzan, or 'storefront_wechat' etc. for our own platform
        self.log_base = dict(
            time=datetime.utcnow().isoformat()
        )
        self.log_base.update(data)

    @cached_property
    def logger_ex(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            out_handler = logging.StreamHandler(sys.stdout)
            out_handler.setFormatter(logging.Formatter("%(message)s"))
            out_handler.setLevel(logging.INFO)
            logger.addHandler(out_handler)
        return logger

    def log_info(self, **kwargs):
        data: dict = kwargs or dict()
        data.update(self.log_base)
        self.logger_ex.info(json_dumps_unicode(data))

    def log_error(self, **kwargs):
        data: dict = kwargs or dict()
        data.update(self.log_base)
        self.logger_ex.error(json_dumps_unicode(data))
