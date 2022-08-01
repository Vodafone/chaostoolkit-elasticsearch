
'''ElasticSearch report tempalte for Chaostoolkit test result. It contains execution general data like start data time
and the Chaostoolkit journey under the result object. '''

message_template = {
        "datasetCategory": "",
        "datasetTopLevelServices": "",
        "datasetType": "chaos",
        "description": "",
        "createdDateTime": "",
        "startDateTime": "",
        "endDateTime": "",
        "environment": "",
        "environmentConfiguration": "",
        "testDetails": {
                "testType": "",
                "testSummary": "",
                "resultStatus": "",
                "releaseName": "",
                "buildNumber": "",
                "result": "object",
                "testAnalysisBy": "",
                "testRecommendations": {
                        "action": "",
                        "description": {
                            "title": "",
                            "text": "",
                            "recommendationType": ""
                        }
                    },
                "testScheduledBy": ""
            },
        "uuid": ""
    }
