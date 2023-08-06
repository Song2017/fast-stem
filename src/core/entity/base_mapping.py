import traceback
from datetime import timedelta
from functools import cached_property
from typing import Any

import arrow
from arrow import Arrow
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.log.log_ex import LogEx


class BaseMapping:
    """
    base mapping for different service providers
    """

    def __init__(self, **data: Any):
        self._context = data.get("context")
        self.logger = LogEx()

    @property
    def now_time_tz(self) -> Arrow:
        return arrow.utcnow()

    @property
    def now_timestamp(self) -> int:
        return (self.now_time_tz + timedelta(hours=8)).int_timestamp

    @cached_property
    def dao(self):
        return None

    async def rpc(self, **kwargs) -> dict:
        """
        consume 3rd-provider service and format for deserialize
        """
        raise NotImplementedError

    async def __call__(self, *args, **kwargs) -> dict:
        """
        request: run > rpc
        run: format for api, db
        rpc: 3rd provider services
        """
        resp_dict = {"code": 400, "message": "service error"}
        self._context = kwargs.get("context")
        req = kwargs.get("body") or dict(kwargs)
        if req and isinstance(req, BaseModel):
            req = req.dict()
        try:
            resp_rpc = await self.rpc(**kwargs)
            resp_dict.update(self.deserialize(resp_rpc))
        except Exception as e:
            self.logger.log_error(**{
                "class": self.__class__.__name__,
                "error": str(e),
                "traceback": str(traceback.format_exc())
            })
            resp_dict["status_code"] = 500
            resp_dict["message"] = str(e)
        finally:
            db: Session = kwargs.get("db")
            self.persistence(db, req=req, resp=resp_dict, input=kwargs)

        return resp_dict

    def persistence(self, db: Session, **kwargs):
        """
        db operation
        """
        ...

    @staticmethod
    def deserialize(resp_rpc):
        """
        deserialize message from 3rd-provider service to api
        """
        return resp_rpc
