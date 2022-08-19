import json
import requests
import sys


def sendAlert(message):
    url = "https://hooks.slack.com/services/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"
    title = "Anomaly Detected :zap:"
    slack_data = {
        "username": "Anomaly Bot",
        "icon_emoji": ":satellite:",
        "channel": "#demo",
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json",
               'Content-Length': byte_length}
    response = requests.post(
        url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
