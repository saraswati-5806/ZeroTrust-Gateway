import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ai.watson_client import watson_client

def handle_chatbot_query(user_message):
    prompt_path = os.path.join(os.path.dirname(__file__), '../ai/prompts/chatbot_system.txt')
    system_prompt = ""
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r') as f:
            system_prompt = f.read()
            
    full_query = f"{system_prompt}\nUser Question: {user_message}"
    response = watson_client.query_watson(full_query)
    return {"response": response}