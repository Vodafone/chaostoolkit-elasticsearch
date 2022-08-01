from typing import TypedDict, List, Optional
from chaoslib.types import Configuration

from .driver import ElasticSearchDriver

__all__ = [
    "is_elasticsearch_running",
]


def is_elasticsearch_running(configuration: Configuration = None):
    es_configuration = configuration.get("elasticsearch")
    host = es_configuration.get("host")
    port = es_configuration.get("port")
    verify_certs = bool(es_configuration.get("verify_certs", True))
    use_ssl = bool(es_configuration.get("use_ssl", True))

    return bool(ElasticSearchDriver(host=host, port=port, verify_certs=verify_certs, use_ssl=use_ssl))
