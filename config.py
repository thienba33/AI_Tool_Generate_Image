import os
from dotenv import load_dotenv

load_dotenv()
def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()

    if not value:
        raise RuntimeError(f"Chưa tìm thấy {name} trong môi trường hoặc .env")

    return value


API_KEY_MODEL_IMAGE = require_env("API_KEY_MODEL_IMAGE")
ACCOUNT_ID = require_env("ACCOUNT_ID")
MODEL = require_env("MODEL")



SYSTEM_PROMPT = """
"""