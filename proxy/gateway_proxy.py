import json
import os
import requests

class GatewayProxy:

    def __init__(self):
        # Corrected path to match config/apps_registry.json location or fallback safely
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/apps_registry.json'))
        if not os.path.exists(config_path):
            config_path = os.path.join(os.path.dirname(__file__), 'apps_registry.json')
            
        with open(config_path) as f:
            registry = json.load(f)
            # Support both list formats or dictionary formats
            if isinstance(registry, dict) and "services" in registry:
                self.apps = {app["id"]: app for app in registry["services"]}
            else:
                self.apps = registry

    def forward(self, app_name, data):
        if app_name not in self.apps:
            return {
                "status": "ERROR",
                "message": "Application not found"
            }

        app = self.apps[app_name]

        try:
            response = requests.post(
                app["url"],
                json=data,
                timeout=5
            )
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }

gateway_proxy = GatewayProxy()