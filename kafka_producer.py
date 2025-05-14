import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer


# Kafka producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


# Kafka topic
topic = "user_events"