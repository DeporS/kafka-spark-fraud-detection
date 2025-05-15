from kafka import KafkaConsumer
import json
from pymongo import MongoClient
from collections import defaultdict, deque
import time

from config import KAFKA_TOPIC as topic


def main():
    # Connecto to MongoDB
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["events"]
    collection = db["logins"]
    alerts = db["alerts"] # weird activity detection

    # Kafka consumer - receiving messages sent by producer
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9093'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Cache for each user_id (in real example it can be substituted with real ip)
    ip_login_times = defaultdict(deque(maxlen=10)) # FIFO queue

    THRESHOLD = 5
    TIME_WINDOW = 10 # in seconds

    # dont know how to name
    try:
        for message in consumer:

            event = message.value
            print(f"Received: {event} - saving to MongoDB.")
            ip = event.get("user_id")
            timestamp = time.time()

            # Save event to MongoDB
            try:
                collection.insert_one(event)
            except Exception as e:
                print("Error saving event to db: ", e)

            if event["event"] == "failed_login":
                # Logic for detecting suspicious ips with failed logins
                ip_login_times[ip].append(timestamp)
                recent_attempts = [t for t in ip_login_times[ip] if timestamp - t < TIME_WINDOW]

                # Too many attempts from one ip
                if len(recent_attempts) >= THRESHOLD:
                    print(f"Too many login attempts from {ip} in {TIME_WINDOW}s!")
                    alerts.insert_one(
                        {
                            "type": "too_many_attempts_from_ip",
                            "ip": ip,
                            "time": timestamp,
                            "attempts": len(recent_attempts)
                        }
                    )



    except KeyboardInterrupt:
            print("Consumer stopped.")


if __name__ == "__main__":
     main()