# ML Interface Service

Asynchronous ML inference using FastAPI + RabbitMQ + Redis

## Overview
This repository implements an asynchronous ML inference pipeline: the API receives raw feature data on `POST /api/v1/inference`, queues preprocessing tasks in RabbitMQ, a worker consumes and preprocesses messages then predicts using a pre-trained scikit-learn model, and the client polls `GET /api/v1/inference/results/{request_id}` for results.

## Structure
- `app/`: FastAPI service
- `worker/`: preprocessing worker
- `ml_model/`: model training and artifact
- `docker-compose.yml`: orchestrates RabbitMQ, Redis, API, worker

## Setup
1. Install dependencies:
   - `pip install -r requirements.txt`
2. Train model:
   - `python ml_model/train_model.py`
3. Run services:
   - `docker-compose up --build`

## API
### POST /api/v1/inference
- Accepts: `sepal_length`, `sepal_width`, `petal_length`, `petal_width` (numbers)
- Returns: `202 Accepted` and `request_id`
- Example:
  ```bash
  curl -X POST http://localhost:8000/api/v1/inference \
    -H 'Content-Type: application/json' \
    -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
  ```

### GET /api/v1/inference/results/{request_id}
- Returns PENDING/COMPLETED/FAILED.
- Example:
  ```bash
  curl http://localhost:8000/api/v1/inference/results/<request_id>
  ```

### GET /health
- Checks RabbitMQ connection and model loaded.

## Local testing
- `pytest app/tests`
- `pytest worker/tests`

## Architecture
- FastAPI endpoint publishes tasks to `preprocessing_queue` (RabbitMQ).
- Worker consumes queue, preprocesses features, uses model to predict.
- Shared state store is Redis, keyed by `request_id`.
- This decoupled approach isolates load-bearing work and enables scaling workers independently.

## Notes
- `.env.example` lists required env variables.
- Both Dockerfiles are multi-stage for smaller image size.
