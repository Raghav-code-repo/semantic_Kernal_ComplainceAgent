# config.py
class Settings:
    OLLAMA_MODEL = "llama3.2:3b"
    ALLOWED_MODELS = ["llama3.2:3b", "llama3.1:8b"]
    REQUIRE_HUMAN_APPROVAL = False  # turn ON later

settings = Settings()