# kernel_factory.py
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion
from config import settings
from logging_conf import audit_logger

def create_kernel() -> Kernel:
    if settings.OLLAMA_MODEL not in settings.ALLOWED_MODELS:
        raise RuntimeError("Model not allow-listed")

    kernel = Kernel()

    kernel.add_service(
        OllamaChatCompletion(
            service_id="ollama",
            ai_model_id=settings.OLLAMA_MODEL
        )
    )

    audit_logger.info(f"Kernel initialized with model={settings.OLLAMA_MODEL}")
    return kernel