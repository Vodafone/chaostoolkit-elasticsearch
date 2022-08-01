from chaoslib import Experiment, Secrets
from chaoslib.run import EventHandlerRegistry, RunEventHandler
from typing import Any, Dict, List, Optional

from logzero import logger

from chaoslib.types import Activity, Run, Configuration, Hypothesis, Journal, Settings
from chaoselasticsearch.driver import ElasticSearchDriver

__all__ = [
    "validate_control",
    "configure_control",
    "cleanup_control",
    "before_experiment_control",
    "after_experiment_control",
    "before_hypothesis_control",
    "after_hypothesis_control",
    "before_method_control",
    "after_method_control",
    "before_activity_control",
    "before_rollback_control",
    "after_rollback_control",
    "after_activity_control",
]

__es__: ElasticSearchDriver = None


def get_elasticsearch_driver() -> ElasticSearchDriver:
    global __es__
    if not __es__:
        raise RuntimeError("Elasticsearch connection is not initialised")
    return __es__


def validate_control(
    experiment: Experiment,
    secrets: Secrets = None,
    event_registry: EventHandlerRegistry = None,
    experiment_ref: str = None,
    trace_id: str = None,
) -> bool:
    return (
        experiment["provider"]["type"] == "python"
        and experiment["provider"]["module"] == "'chaoselasticsearch.controls.es'"
    )


def configure_control(
    experiment: Experiment,
    configuration: Configuration = None,
    secrets: Secrets = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    verify_certs: Optional[bool] = None,
    use_ssl: Optional[bool] = None,
    index: Optional[str] = None
) -> None:
    global __es__
    elasticsearch_configuration = configuration.get("elasticsearch", {})

    if not host:
        host = elasticsearch_configuration.get("host")
    if not port:
        port = elasticsearch_configuration.get("port")
    if not index:
        index = elasticsearch_configuration.get("index")

    if verify_certs is None:
        verify_certs = bool(elasticsearch_configuration.get("verify_certs", True))
    if use_ssl is None:
        use_ssl = bool(elasticsearch_configuration.get("use_ssl", True))

    if not host and not port:
        raise RuntimeError("Elasticsearch configuration is missing")

    logger.debug(
        f"Elasticsearch configure control. Host: {host} Port: {port} Verify cert: {verify_certs} Use_ssl: {use_ssl} Index: {index}"
    )

    __es__ = ElasticSearchDriver(host=host, port=port, verify_certs=verify_certs, use_ssl=use_ssl, index=index)

    logger.info("Elasticsearch control configured correctly")
    if __es__ is None:
        logger.error("Failed to setup Elasticsearch control")
        raise RuntimeError("Elasticsearch connection failed")


def before_experiment_control(
    context: Experiment, configuration: Configuration = None, secrets: Secrets = None, **kwargs
):
    environment = configuration.get("environment")
    services = configuration.get("service_name")
    logger.debug("Before experiment control. Initialising elasticsearch connection.")
    driver = get_elasticsearch_driver()
    driver.create_document({services}, environment, "chaos", "user tbd", "release name tbd", "build number tbd")


def after_experiment_control(
    context: Experiment, state: Journal, configuration: Configuration = None, secrets: Secrets = None, **kwargs
):
    driver = get_elasticsearch_driver()
    driver.update_document_with_result("after_experiment_control", state)


def before_activity_control(context: Activity, *args, **kwargs) -> None:
    _update_status("before_activity_control", context["type"], context["name"])


def after_activity_control(context: Activity, state: Run, *args, **kwargs) -> None:
    _update_status("after_activity_control", context["type"], context["name"])


def cleanup_control():
    pass

def before_loading_experiment_control(context: str, **kwargs):
    pass


def after_loading_experiment_control(context: str, state: Experiment, **kwargs):
    pass


def before_hypothesis_control(
    context: Hypothesis, configuration: Configuration = None, secrets: Secrets = None, **kwargs
):
    _update_status("before_hypothesis_control", "hypothesis", context["title"])


def after_hypothesis_control(
    context: Hypothesis, state: Dict[str, Any], configuration: Configuration = None, secrets: Secrets = None, **kwargs
):
    _update_status("after_hypothesis_control", "hypothesis", context["title"])


def before_method_control(context: Experiment, configuration: Configuration = None, secrets: Secrets = None, **kwargs):
    _update_status("before_method_control", "method", context["title"])


def after_method_control(
    context: Experiment, state: List[Run], configuration: Configuration = None, secrets: Secrets = None, **kwargs
):
    _update_status("after_method_control", "method", context["title"])


def before_rollback_control(
    context: Experiment, configuration: Configuration = None, secrets: Secrets = None, **kwargs
):
    _update_status("before_rollback_control", "rollback", context["title"])


def after_rollback_control(
    context: Experiment, state: List[Run], configuration: Configuration = None, secrets: Secrets = None, **kwargs
):
    _update_status("after_rollback_control", "rollback", context["title"])


def _update_status(stage_name: str, type: str, name: str):
    logger.debug(f"Updating status for stage: {stage_name}")

    driver = get_elasticsearch_driver()
    driver.update_document_status(f"Stage: {stage_name}. Type: {type} Name: {name}")
