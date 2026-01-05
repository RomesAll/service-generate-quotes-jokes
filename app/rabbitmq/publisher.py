from pika import ConnectionParameters, PlainCredentials, BlockingConnection
from datetime import datetime, timezone
from app.core import settings

connection_parameters = ConnectionParameters(
    host=settings.rabbitmq.mq_host,
    port=settings.rabbitmq.mq_port,
    credentials=PlainCredentials(username=settings.rabbitmq.mq_user, password=settings.rabbitmq.mq_password)
)

def get_connection():
    return BlockingConnection(parameters=connection_parameters)

def create_message(event, context):
    return f'{event}: {context} (datetime: {datetime.now(tz=timezone.utc).strftime('%d/%m/%Y, %H:%M:%S')})'

def publish_message(event, context):
    with get_connection() as connection:
        with connection.channel() as channel:
            channel.exchange_declare(exchange_type='direct', exchange='message_exchange', durable=True)
            channel.exchange_declare(exchange_type='direct', exchange='dlx_exchange', durable=True)
            message_queue = channel.queue_declare(queue='message_queue', durable=True,
                                                arguments={'x-dead-letter-exchange': 'dlx_exchange',
                                                           'x-dead-letter-routing-key': 'dlx_key',
                                                           'x-max-length-bytes': 100})
            dlx_queue = channel.queue_declare(queue='dlx_queue', durable=True)
            channel.queue_bind(exchange='message_exchange', queue=message_queue.method.queue, routing_key='message_key')
            channel.queue_bind(exchange='dlx_exchange', queue=dlx_queue.method.queue, routing_key='dlx_key')
            channel.basic_publish(exchange='message_exchange', routing_key='message_key', body=create_message(event, context))

if __name__ == '__main__':
    publish_message(event='create user', context='roman beskokotov')