import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    MODEL_PATH = os.getenv('MODEL_PATH', '/app/ml_model/model.pkl')
    PREPROCESSING_DELAY_SECONDS = int(os.getenv('PREPROCESSING_DELAY_SECONDS', 2))
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))

settings = Settings()
