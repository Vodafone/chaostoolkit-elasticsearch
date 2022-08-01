import logging

import elasticsearch
from logzero import logger
import uuid
from datetime import datetime
from typing import List

from .entity import message_template

ISO_8601_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class ElasticSearchDriver():
    def __init__(
            self, host: str = None, port: int = None, use_ssl: bool = True, verify_certs: bool = True,
            index: str = "chaos"
    ):
        self.host = host
        self.port = port
        es_options = {'use_ssl': use_ssl, 'verify_certs': verify_certs}
        es_connect_options = {'retry_on_timeout': True, 'max_retries': 5, 'timeout': 30, **es_options}
        try:
            host_url = f"{self.host}:{self.port}"
            self.es_client = elasticsearch.Elasticsearch(host_url, **es_connect_options)
            self.es_client.cluster.health()
        except Exception as Err:
            logging.error(Err)

        # Creating document from template
        self.doc = message_template
        self.index = index
        self.doc_id = ""
        self.test_type = ""
        self.top_level_services = ""
        self.environment_name = ""
        self.test_scheduled_by = ""
        self.release_name = ""
        self.build_number = ""

    def create_document(
            self,
            top_level_services: List[str],
            environment_name: str,
            test_type: str,
            test_scheduled_by: str,
            release_name: str,
            build_number: str,
    ):

        # Updating document using function parameters
        self.doc_id = str(uuid.uuid4().hex)
        self.test_type = test_type
        self.top_level_services = top_level_services
        self.environment_name = environment_name
        self.test_scheduled_by = test_scheduled_by
        self.release_name = release_name
        self.build_number = build_number

        self.doc["datasetCategory"] = "single-container"
        # self.doc['datasetTopLevelServices'] = self.top_level_services
        self.doc["datasetType"] = self.test_type
        self.doc["description"] = "Chaos test run"
        self.doc["createdDateTime"] = datetime.now().astimezone().strftime(ISO_8601_FORMAT)
        self.doc["startDateTime"] = datetime.now().astimezone().strftime(ISO_8601_FORMAT)
        self.doc["endDateTime"] = None
        self.doc["environment"] = self.environment_name
        self.doc["environmentConfiguration"] = None
        self.doc["uuid"] = self.doc_id

        self.doc["testDetails"]["resultStatus"] = "started"
        self.doc["testDetails"]["releaseName"] = self.release_name
        self.doc["testDetails"]["buildNumber"] = self.build_number
        self.doc["testDetails"]["testScheduledBy"] = self.test_scheduled_by
        self.doc["testDetails"]["result"] = None
        self.doc["testDetails"]["testRecommendations"]["description"] = None

        try:
            response = self.es_client.index(self.index, id=str(self.doc_id), body=self.doc)
            if 'result' in response and response['result'] != 'created':
                logger.debug(response)
                raise RuntimeError("Could not create elasticsearch document")
        except Exception as Err:
            logger.error(Err)

    def update_document_status(self, status: str):
        self.doc["testDetails"]["resultStatus"] = status
        try:
            response = self.es_client.index(self.index, id=str(self.doc_id), body=self.doc)
            if 'result' in response and response['result'] != 'updated':
                logger.debug(response)
                raise RuntimeError("Could not update elasticsearch document")
        except Exception as Err:
            logger.error(Err)

    def update_document_with_result(self, status: str, journey: str):
        self.doc["testDetails"]["resultStatus"] = status
        self.doc["endDateTime"] = datetime.now().astimezone().strftime(ISO_8601_FORMAT)
        self.doc["testDetails"]["result"] = journey
        try:
            response = self.es_client.index(self.index, id=str(self.doc_id), body=self.doc)
            if 'result' in response and response['result'] != 'updated':
                logger.debug(response)
                raise RuntimeError("Could not update elasticsearch document with result")
        except Exception as Err:
            logger.error(Err)
