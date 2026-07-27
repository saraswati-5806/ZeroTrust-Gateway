import json
import requests


class GatewayProxy:

    def __init__(self):

        with open("backend/data/micro_apps.json") as f:
            self.apps = json.load(f)

    def forward(self, app_name, data):

        if app_name not in self.apps:
            return {
                "status": "ERROR",
                "message": "Application not found"
            }

        app = self.apps[app_name]

        response = requests.post(
            app["url"],
            json=data,
            timeout=5
        )

        return response.json()


gateway_proxy = GatewayProxy()