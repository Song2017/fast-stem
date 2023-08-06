import logging
import os
import sys
from functools import cached_property
from stem.pkg.monitor import Monitor


class Connector:
    """
    Connector, connect app context and business.
    """

    @cached_property
    def os_conf(self) -> dict:
        return dict(os.environ)

    @cached_property
    def app_cong(self) -> dict:
        return {}

    @cached_property
    def monitor(self):
        return Monitor()

    @cached_property
    def logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            out_handler = logging.StreamHandler(sys.stdout)
            out_handler.setFormatter(logging.Formatter('%(message)s'))
            out_handler.setLevel(logging.INFO)
            logger.addHandler(out_handler)
        return logger
