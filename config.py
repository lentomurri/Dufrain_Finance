import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "model": os.getenv("OPENAI_MODEL", "gpt-4o"),
    "embedding_model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    "inputs": {
        "models": "inputs/models/",
        "data": "inputs/data/",
        "knowledge": "inputs/knowledge/",
    },
    "output": {
        "reports": "output/reports/",
    },
}

def validate_config(cfg: dict) -> None:
    """
    Validate required config values are present.

    Raises:
        ValueError: If a required value is missing.
    """
    if not cfg.get("openai_api_key"):
        raise ValueError("OPENAI_API_KEY is not set. Add it to your .env file.")
