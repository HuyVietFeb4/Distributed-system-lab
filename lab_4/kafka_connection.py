from confluent_kafka import Consumer, KafkaError, Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

class kafka_connection:
    def __init__(self, group_id):
        self.consumer_conf = { 'bootstrap.servers': 'localhost:9094,localhost:9095', 'group.id': group_id, 'auto.offset.reset': 'earliest' }
        self.producer_conf = { 'bootstrap.servers': 'localhost:9094,localhost:9095' }
    def consume(self, topic):
        consumer = Consumer(self.consumer_conf)
        consumer.subscribe([topic])
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

    def produce(self, topic, message):
        producer = Producer(self.producer_conf)
        producer.produce(topic, message, callback=delivery_report)
        producer.poll(0) # Trigger delivery callback
        producer.flush() # Wait for all messages to be delivered callback
