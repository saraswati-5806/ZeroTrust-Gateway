import os
import requests

class WatsonXClient:
    def __init__(self):
        self.api_key = os.getenv("WATSON_API_KEY", "")
        self.project_id = os.getenv("WATSON_PROJECT_ID", "")
        self.url = os.getenv("WATSON_URL", "https://us-south.ml.cloud.ibm.com")

    def generate_explanation(self, context_data):
        prompt_path = os.path.join(os.path.dirname(__file__), 'prompts/threat_explain.txt')
        try:
            with open(prompt_path, 'r') as f:
                prompt_template = f.read()
            
            formatted_prompt = prompt_template.format(**context_data)
            
            if not self.api_key:
                return self._fallback_explanation(context_data)
                
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            payload = {
                "input": formatted_prompt,
                "parameters": {
                    "decoding_method": "greedy",
                    "max_new_tokens": 150,
                    "stop_sequences": ["USER:"]
                },
                "model_id": "ibm/granite-13b-instruct-v2",
                "project_id": self.project_id
            }
            
            response = requests.post(f"{self.url}/ml/v1/text/generation?version=2023-05-29", json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                result = response.json()
                return result['results'][0]['generated_text'].strip()
            else:
                return self._fallback_explanation(context_data)
                
        except Exception as e:
            return self._fallback_explanation(context_data)

    def _fallback_explanation(self, data):
        signals = ", ".join(data.get('signals', ['STANDARD_CHECK']))
        return f"This access attempt received a risk score of {data.get('risk_score')}/100 and decision '{data.get('decision')}' due to triggered risk indicators: {signals}."

watson_client = WatsonXClient()