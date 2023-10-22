import os
import requests


class TextSender:

    def __init__(self):
        # Authentication variables. A Sinch account is needed to obtain these, as well as
        # a desired phone number to send the notification to.
        self.servicePlanId = os.environ['servicePlanId']
        self.apiToken = os.environ['apiToken']
        self.sinchNumber = os.environ['sinchNumber']
        self.toNumber = os.environ['toNumber']
        self.url = "https://us.sms.api.sinch.com/xms/v1/" + self.servicePlanId + "/batches"

        self.headers = {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + self.apiToken
        }

    def send_text(self, body: str):
        payload = {
          "from": self.sinchNumber,
          "to": [
            self.toNumber
          ],
          "body": body
        }

        # Sends the text.
        response = requests.post(self.url, json=payload, headers=self.headers)
        # Checks if the text successfully went through. Raises an error if not.
        print(f"Errors in texting: {response.raise_for_status()}")
