import os
import requests


class TextSender:

    def __init__(self):

        self.servicePlanId = os.environ['servicePlanId']
        self.apiToken = os.environ['apiToken']
        self.sinchNumber = os.environ['sinchNumber']
        self.toNumber = os.environ['toNumber']
        self.url = "https://us.sms.api.sinch.com/xms/v1/" + self.servicePlanId + "/batches"

        self.payload = {
          "from": self.sinchNumber,
          "to": [
            self.toNumber
          ],
          "body": "This is a test"
        }

        self.headers = {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + self.apiToken
        }

    def send_text(self, body: str):
        self.payload['body'] = body

        response = requests.post(self.url, json=self.payload, headers=self.headers)
        print(response.status_code)
