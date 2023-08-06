from prometheus_client import Counter, Gauge, Summary
from prometheus_client.core import CollectorRegistry

from stem import Singleton


class Monitor(metaclass=Singleton):
    def __init__(self):
        self.collector_registry = CollectorRegistry(auto_describe=False)
        self.request_time_max_map = {}

        self.summary = Summary(
            name="http_server_requests_seconds",
            documentation="Num of request time summary",
            registry=self.collector_registry)

        self.max_cost = Gauge(
            name="http_server_requests_seconds_max",
            documentation="Number of request max cost",
            registry=self.collector_registry)

        self.fail_count = Counter(
            name="http_server_requests_error",
            documentation="Times of request fail in total",
            registry=self.collector_registry)
