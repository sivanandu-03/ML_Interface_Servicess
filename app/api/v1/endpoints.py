from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uuid
import json
import logging

from app.services.mq_service import MessageQueueService
from app.core.store import set_result, get_result

router = APIRouter()

mq_service = MessageQueueService()


class RawFeatures(BaseModel):
    sepal_length: float = Field(...)
    sepal_width: float = Field(...)
    petal_length: float = Field(...)
    petal_width: float = Field(...)


class InferenceRequestResponse(BaseModel):
    request_id: str
    status: str
    message: str


class InferenceResultResponse(BaseModel):
    request_id: str
    status: str
    prediction: Optional[Any] = None
    processed_features: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


@router.post('/inference', response_model=InferenceRequestResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_inference_request(raw_features: RawFeatures):
    request_id = str(uuid.uuid4())
    request_payload = raw_features.dict()

    set_result(request_id, {'status': 'PENDING', 'raw_features': request_payload})

    try:
        message = json.dumps({'request_id': request_id, 'features': request_payload})
        await mq_service.publish_message(message)
        logging.info('Published request_id %s to preprocessing queue.', request_id)
        return InferenceRequestResponse(
            request_id=request_id,
            status='ACCEPTED',
            message='Inference request accepted for asynchronous processing.',
        )
    except Exception as e:
        logging.error('Failed to publish message for request_id %s: %s', request_id, e, exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to submit inference request')


@router.get('/inference/results/{request_id}', response_model=InferenceResultResponse)
async def get_inference_result(request_id: str):
    result = get_result(request_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Request ID not found.')

    status_value = result.get('status')
    if status_value == 'COMPLETED':
        return InferenceResultResponse(
            request_id=request_id,
            status='COMPLETED',
            prediction=result.get('prediction'),
            processed_features=result.get('processed_features'),
            message='Inference completed',
        )
    elif status_value == 'FAILED':
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Inference processing failed.')
    else:
        return InferenceResultResponse(
            request_id=request_id,
            status='PENDING',
            message='Processing in progress, please try again later.',
        )
