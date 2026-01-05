from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from datetime import datetime, timezone

connection_parameters = ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=PlainCredentials(username='guest', password='guest')
)

def get_connection():
    return BlockingConnection(parameters=connection_parameters)

def processing_message(ch, method, properties, body: bytes):
    try:
        with open('./log_queue_message.txt', 'a') as f:
            f.write(f'{datetime.now(tz=timezone.utc).strftime('%d/%m/%Y, %H:%M:%S')} - {body.decode("utf-8")}\n')
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    with get_connection() as connection:
        with connection.channel() as channel:
            channel.exchange_declare(exchange_type='direct', exchange='message_exchange', durable=True)
            message_queue = channel.queue_declare(queue='message_queue', durable=True,
                                                  arguments={'x-dead-letter-exchange': 'dlx_exchange',
                                                             'x-dead-letter-routing-key': 'dlx_key',
                                                             'x-max-length-bytes': 100})
            channel.queue_bind(exchange='message_exchange', queue=message_queue.method.queue, routing_key='message_key')
            channel.basic_consume(queue=message_queue.method.queue, auto_ack=False, on_message_callback=processing_message)
            channel.start_consuming()

if __name__ == "__main__":
    main()