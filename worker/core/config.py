import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
    MODEL_PATH = os.getenv("MODEL_PATH")
    PREPROCESSING_DELAY_SECONDS = int(os.getenv("PREPROCESSING_DELAY_SECONDS", 2))

settings = Settings()
