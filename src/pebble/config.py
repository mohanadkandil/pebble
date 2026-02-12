import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY")
    model: str

@lru_cache
def get_settings() -> Settings:
    return Settings(
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        model=os.getenv("MODEL"),
    )