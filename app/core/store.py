import json
import redis
from app.core.config import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB, decode_responses=True)


def set_result(request_id: str, value: dict):
    redis_client.set(request_id, json.dumps(value))


def get_result(request_id: str):
    value = redis_client.get(request_id)
    if value is None:
        return None
    return json.loads(value)


def delete_result(request_id: str):
    redis_client.delete(request_id)
