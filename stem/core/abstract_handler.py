import datetime
import traceback
from typing import Dict

from stem.core.handler import Handler


class AbstractHandler:
    PLATFORM = "HANDLER"

    def __init__(
            self,
            python_params: dict = None,
            _input: dict = None,
            connector_instance=None
    ):
        self.input = dict(_input or {})
        self.merchant_id: str = self.input.get("merchant", "")
        self.original_python_params = dict(python_params or {})
        self.body: dict = self.original_python_params.get("input_body")
        self.connector_instance = connector_instance
        self.request: dict = {}
        self.response: dict = {}

    def __call__(self, *args, **kwargs):
        begin_time = datetime.datetime.utcnow()
        mapping: Handler = self.rpc_mapping() or self

        response = mapping.rpc_check()
        if response:
            return response, 400

        # format input data and copy to self.request
        mapping.request = mapping.serialize()

        # call third party service
        mapping.run()

        # format output data
        mapping.monitor_observe(begin_time)
        resp = mapping.deserialize()
        status_code = None
        if isinstance(resp, Dict):
            status_code = resp.get("status_code") or resp.get("code")
        return resp, status_code

    def rpc_mapping(self):
        # return mapping implementation based on the input parameter
        pass

    def rpc_check(self):
        # merchant should have received token
        if not self.conf:
            return self.custom_response(
                f"Merchant '{self.merchant_id}' is invalid")

    def serialize(self):
        return self.input

    def rpc_base(self) -> dict:
        # execute to call third party service
        raise NotImplementedError("#rpc_base")

    def api(self) -> tuple:
        """
        The configuration of API, the last two parameters could be ignored.
         e.g.
          ("orders")
          ("GET", "orders", {})
        """
        return ()

    def run(self):
        try:
            rpc_response: dict = self.rpc_base()
            self.response.update(rpc_response)
            # mask token_info
            _input_copy = dict(self.input)
            _input_copy.update({"token_info": "***"})
            self.log_info({
                "input": str(_input_copy),
                "request": str(self.request),
                "response": str(self.response),
            })
        except Exception as e:
            self.monitor.fail_count.inc()
            except_message: str = "{0}\n{1}".format(
                type(e).__name__, str(e))
            self.response["code"] = 500
            self.response["error"] = except_message
            self.response["error"] = "{0}\n{1}".format(
                except_message, traceback.format_exc())
            self.log_error(self.response)

    def pre_deserialize(self) -> Dict:
        # prepare response message
        return dict()

    def persistence(self, resp: dict):
        # save data to DB
        pass

    def deserialize(self):
        # derived class can overwrite this function
        resp: dict = self.pre_deserialize()
        return resp

    def custom_response(self, message: str = "", code: int = 400,
                        is_log=False):
        if is_log is True:
            _input_copy = dict(self.input)
            _input_copy.update({"token_info": "***"})
            self.log_info({
                "request": _input_copy,
                "response": message
            })
        return dict(message=message, code=code)

    def base_log(self) -> dict:
        return {
            "smklog.platform": self.PLATFORM,
            "smklog.source": "",
            "smklog.label": str(self.__class__.__name__),
            "smklog.timing": datetime.datetime.utcnow().isoformat(),
            "smklog.user": self.merchant_id,
            "smklog.service": 'payment service',
        }
