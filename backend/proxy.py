"""
Identity Aware Proxy

Receives requests

↓

Evaluates Zero Trust Policies

↓

Routes to Internal Application
"""

import json
import requests

from policy_engine import policy_engine


class IdentityAwareProxy:

    def __init__(self):

        with open(
            "backend/data/micro_apps.json",
            "r"
        ) as file:

            self.apps = json.load(file)

    # ----------------------------------------------

    def get_target(self, app_name):

        return self.apps.get(app_name)

    # ----------------------------------------------

    def forward(self, app_name, request_data):

        result = policy_engine.evaluate(request_data)

        if not result["allow"]:

            return {

                "status": "DENIED",
                "policy": result

            }

        app = self.get_target(app_name)

        if app is None:

            return {

                "status": "ERROR",
                "message": "Application Not Found"

            }

        try:

            response = requests.post(

                app["url"],

                json=request_data,

                timeout=5

            )

            return {

                "status": "SUCCESS",
                "target": app["name"],
                "response": response.json(),
                "policy": result

            }

        except Exception as e:

            return {

                "status": "FAILED",
                "message": str(e)

            }


proxy = IdentityAwareProxy()