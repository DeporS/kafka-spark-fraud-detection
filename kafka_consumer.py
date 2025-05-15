from kafka import KafkaConsumer
import json
from pymongo import MongoClient

from config import KAFKA_TOPIC as topic


def main():
    # Connecto to MongoDB
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["events"]
    collection = db["logins"]


    # Kafka consumer - receiving messages sent by producer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9093'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    try:
        for message in consumer:
            print(f"Received: {message.value} - saving to MongoDB.")
            try:
                collection.insert_one(message.value)
            except Exception as e:
                print("Error saving event to db: ", e)

    except KeyboardInterrupt:
            print("Consumer stopped.")


if __name__ == "__main__":
     main()