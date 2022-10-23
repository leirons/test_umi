import os


class Config:
    DATABASE_URL = os.getenv(
        "database_url",
        default="postgresql+psycopg2://postgres:grecigor3004@localhost/todo")
    # Я сначала реализовал свой метод, но вспомнил, что уже есть готовый
    REDIS = os.getenv("redis", default="localhost:6379")
    CACHE = {
        "DEBUG": True,
        "CACHE_TYPE": "SimpleCache",
        "CACHE_DEFAULT_TIMEOUT": 300
    }
