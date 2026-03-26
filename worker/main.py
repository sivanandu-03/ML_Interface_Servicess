import asyncio
import json
import logging

import aio_pika

from worker.core.config import settings
from worker.core.preprocessing import preprocess_features
from app.services.ml_service import MLService
from app.core.store import set_result, get_result

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def process_task(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            payload = json.loads(message.body.decode('utf-8'))
            request_id = payload.get('request_id')
            raw_features = payload.get('features')

            if not request_id or not isinstance(raw_features, dict):
                logger.error('Invalid message payload: %s', payload)
                await message.reject(requeue=False)
                return

            current = get_result(request_id)
            if current and current.get('status') == 'COMPLETED':
                logger.info('Request %s already completed. ACKing.', request_id)
                return

            logger.info('Worker starts processing request %s', request_id)
            await asyncio.sleep(settings.PREPROCESSING_DELAY_SECONDS)
            processed_features = preprocess_features(raw_features)
            prediction = worker_ml_service.predict(processed_features)

            set_result(request_id, {
                'status': 'COMPLETED',
                'prediction': prediction,
                'processed_features': processed_features,
            })
            logger.info('Worker completed request %s prediction=%s', request_id, prediction)

        except Exception as err:
            logger.exception('Failed to process message')
            if request_id:
                set_result(request_id, {'status': 'FAILED', 'error': str(err)})
            await message.reject(requeue=False)
            return


async def consume_messages():
    logger.info('Worker starting up...')
    connection = await aio_pika.connect_robust(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        login=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('preprocessing_queue', durable=True)
        logger.info('Worker connected to RabbitMQ, waiting messages...')

        await queue.consume(process_task)

        # Keep running
        while True:
            await asyncio.sleep(1)


if __name__ == '__main__':
    worker_ml_service = MLService(settings.MODEL_PATH)
    worker_ml_service.load_model()

    try:
        asyncio.run(consume_messages())
    except KeyboardInterrupt:
        logger.info('Worker shutdown via KeyboardInterrupt')
