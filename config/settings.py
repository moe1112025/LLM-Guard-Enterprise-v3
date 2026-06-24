# config/settings.py
APP_NAME = "LLM-GUARD v3.0: Enterprise Semantic Benchmarking Suite"
VERSION = "3.0.0"

MODEL_PARAMS = {
    "temperature": 0.0,
    "top_p": 0.1,
    "seed": 42
}

TARGET_MODELS = ["llama3"]
JUDGE_MODEL = "llama3"