"""Top package for chaoselasticsearch."""
from typing import List
from logzero import logger

from chaoslib.discovery.discover import discover_actions, discover_probes, \
    initialize_discovery_result, discover_activities
from chaoslib.types import Discovery, DiscoveredActivities

name = "chaoselasticsearch"
__author__ = """Gabor Gerencser"""
__email__ = 'gabor.gerencser@vodafone.com'
__version__ = '0.0.1'
__all__ = ["discover", "__version__"]


def discover(discover_system: bool = True) -> Discovery:
    logger.info("Discovering capabilities from chaostoolkit-elasticsearch")

    discovery = initialize_discovery_result(
        "chaoselasticsearch", __version__, "elasticsearch")
    discovery["activities"].extend(load_exported_activities())
    return discovery

def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_probes("chaoselasticsearch.probes"))
    activities.extend(discover_activities("chaoselasticsearch.controls.es","control"))
    return activities
