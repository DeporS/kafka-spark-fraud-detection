from kafka import KafkaConsumer
import json
from kafka_producer import topic


consumer = KafkaConsumer(
    topic,
    bootstrap_servers=['localhost:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

try:
    for message in consumer:
        print("Received: ", message.value)
        
except KeyboardInterrupt:
        print("Consumer stopped.")