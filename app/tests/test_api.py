import json
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1 import endpoints
from app.core.store import redis_client

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_store():
    redis_client.flushdb()
    yield


def test_post_inference_accepts_request(monkeypatch):
    async def fake_publish(message):
        assert 'request_id' in json.loads(message)

    monkeypatch.setattr(endpoints, 'mq_service', endpoints.mq_service)
    monkeypatch.setattr(endpoints.mq_service, 'publish_message', fake_publish)

    payload = {
        'sepal_length': 5.1,
        'sepal_width': 3.5,
        'petal_length': 1.4,
        'petal_width': 0.2,
    }
    resp = client.post('/api/v1/inference', json=payload)
    assert resp.status_code == 202
    data = resp.json()
    assert 'request_id' in data
    assert data['status'] == 'ACCEPTED'


def test_get_result_not_found():
    resp = client.get('/api/v1/inference/results/does-not-exist')
    assert resp.status_code == 404


def test_get_result_pending():
    request_id = 'test-pending-id'
    redis_client.set(request_id, json.dumps({'status': 'PENDING'}))
    resp = client.get(f'/api/v1/inference/results/{request_id}')
    assert resp.status_code == 200
    body = resp.json()
    assert body['status'] == 'PENDING'
