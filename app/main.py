from fastapi import FastAPI, HTTPException, status
import logging

from app.core.config import settings
from app.services.mq_service import MessageQueueService
from app.services.ml_service import MLService
from app.api.v1 import endpoints

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title='ML Inference Service',
    description='API for asynchronous ML model inference with preprocessing queue.',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
)

mq_service = endpoints.mq_service
ml_service = MLService(settings.MODEL_PATH)


@app.on_event('startup')
async def startup_event():
    logging.info('Starting up ML Inference Service...')
    await mq_service.connect()
    ml_service.load_model()
    logging.info('ML Inference Service started successfully.')


@app.on_event('shutdown')
async def shutdown_event():
    logging.info('Shutting down ML Inference Service...')
    await mq_service.disconnect()
    logging.info('ML Inference Service shut down.')


@app.get('/health', summary='Health Check')
async def health_check():
    if mq_service._connection and not mq_service._connection.is_closed and ml_service.is_model_loaded():
        return {'status': 'ok', 'message': 'Service is healthy and operational'}
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Service is not ready')


app.include_router(endpoints.router, prefix='/api/v1', tags=['Inference'])
