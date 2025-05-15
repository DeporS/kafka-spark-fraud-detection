from kafka import KafkaConsumer
import json
from db import logins_collection, alerts_collection
from alert_detector import AlertDetector
from config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS


def consume_events():
    # Kafka consumer - receiving messages sent by producer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='latest', # earliest czyta od poczatku
        enable_auto_commit=True,
        group_id='my-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    detector = AlertDetector()


    try:
        for message in consumer:
            event = message.value
            print(f"Received: {event}")

            # Save event to events collection
            try:
                logins_collection.insert_one(event)
            except Exception as e:
                print("Error saving event to db: ", e)

            # detect alerts
            alerts = detector.process_event(event)

            # Save alerts to alerts collection
            for alert in alerts:
                try:
                    alerts_collection.insert_one(alert)
                    print("Alert generated:", alert)
                except Exception as e:
                    print("Error saving alert:", e)

    except KeyboardInterrupt:
            print("Consumer stopped.")


if __name__ == "__main__":
    consume_events()