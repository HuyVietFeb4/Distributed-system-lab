from confluent_kafka import Producer, Consumer, KafkaError
import time, threading

producer_conf = { 'bootstrap.servers': 'localhost:9094,localhost:9095' }
consumer_conf = { 'bootstrap.servers': 'localhost:9094,localhost:9095', 'group.id': 'hollllla', 'auto.offset.reset': 'earliest' }

def consume():
    # use earliest to fetch all data and latest to fetch new data only
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['monitor'])
    try:
        while True:
            msg = consumer.poll(1.0) # timeout in seconds
            if msg is None:
                # print('No message recieved')
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                break
            print(f"Received message: {msg.value().decode('utf-8')} from {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
    except KeyboardInterrupt:
        print("Stopping consumer")
    finally:
        consumer.close()


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce():
    while True:
        try:
            producer = Producer(producer_conf)
            for i in range(10):
                message = 'hostname -I'
                print(f'Produce to cmd topic message: {message}')
                producer.produce('cmd', message.encode('utf-8'), callback=delivery_report)
                producer.poll(0) # Trigger delivery callback

            producer.flush() # Wait for all messages to be delivered callback
            time.sleep(5)
        except KeyboardInterrupt:
            print("Stopping consumer")
        finally:
            producer.close()


if __name__ == "__main__":
    ConsumerThread = threading.Thread(target=consume)
    ConsumerThread.start()
    ProducerThread = threading.Thread(target=produce)
    ProducerThread.start()
    try:
        ConsumerThread.join()
        ProducerThread.join()
    except KeyboardInterrupt:
        pass