# connectors/ollama_connector.py
import requests
from core.base_connector import BaseLLMConnector
from config.settings import MODEL_PARAMS

class AdvancedOllamaConnector(BaseLLMConnector):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.endpoint = "http://localhost:11434/api/generate"

    def connect(self) -> bool:
        try:
            response = requests.get("http://localhost:11434", timeout=2)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def send_query(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": MODEL_PARAMS
        }
        try:
            response = requests.post(self.endpoint, json=payload, timeout=25)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            return f"[ERROR] Code {response.status_code}"
        except requests.RequestException:
            return "[ERROR] Connection Timeout"