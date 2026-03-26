import aio_pika
import logging
from app.core.config import settings

log = logging.getLogger(__name__)


class MessageQueueService:
    def __init__(self):
        self._connection = None
        self._channel = None

    async def connect(self):
        if self._connection and not self._connection.is_closed:
            return
        self._connection = await aio_pika.connect_robust(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
        )
        self._channel = await self._connection.channel()
        await self._channel.declare_queue('preprocessing_queue', durable=True)
        log.info('Connected to RabbitMQ')

    async def disconnect(self):
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        self._connection = None
        self._channel = None

    async def publish_message(self, message: str):
        if self._connection is None or self._connection.is_closed:
            await self.connect()
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=message.encode('utf-8'), delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key='preprocessing_queue',
        )
        log.debug('Published message to preprocessing_queue')
