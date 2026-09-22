import os
from dotenv import load_dotenv
from system_prompt import SYSTEM_PROMPT

load_dotenv()
def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()

    if not value:
        raise RuntimeError(f"Chưa tìm thấy {name} trong môi trường hoặc .env")

    return value


MODEL = require_env("MODEL")
API_KEY_HOST = require_env("API_KEY_HOST")
URL_HOST = require_env("URL_HOST")

SIZE_IMAGE = {
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
}
MAX_INPUT_IMAGES = 3
MAX_INPUT_FILES = 3
SIZE_STORAGE_IMAGES = 7_000_000
SIZE_STORAGE_TEXT = 7_000_000
SIZE_STORAGE_FILE = 50_000_000
MAX_PAGES = 3
IMAGES_FORMATS = ['PNG','JPEG', 'WEBP', 'HEIC','HEIF']
def build_system_prompt(knowledge: str = "") -> str:
    return SYSTEM_PROMPT.replace("{{knowledge}}", knowledge)