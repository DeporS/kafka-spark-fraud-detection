import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

from config import KAFKA_TOPIC as topic


# Kafka producer
try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9093'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    print("Kafka not reachable:", e)
    exit(1)


KNOWN_IPS = [f"192.168.1.{i}" for i in range(1, 101)]

def generate_login_events():
    """This function generates realistic login event data"""
    cities = ["Poznan", "Wroclaw", "Warszawa", "Gdansk", "Krakow", "Berlin", "Moskov", "NYC"]
    devices = ["PC", "Mobile", "Unknown"]
    events = ["login", "logout", "failed_login", "session_timeout"]
    

    city_weights = [1, 1, 3, 1, 2, 5, 5, 10]
    device_weights = [1, 5, 0.2]
    event_weights = [5, 3, 2, 2]

    login_event = {
        "ip_address": random.choice(KNOWN_IPS),
        "event": random.choices(events, weights=event_weights, k=1)[0],
        "timestamp": datetime.utcnow().isoformat(),
        "device": random.choices(devices, weights=device_weights, k=1)[0],
        "location": random.choices(cities, weights=city_weights, k=1)[0]
    }

    return login_event


if __name__ == '__main__':
    try:
        while True:
            # Generate event data
            event = generate_login_events()
            
            # Send generated event to Kafka
            try:
                producer.send(topic, event)
                print("Producer event: ", event)
            except Exception as e:
                print("Error sending event to Kafka:", e)

            # Wait 1 sec before sending next event
            time.sleep(1)

    except KeyboardInterrupt:
        print("Producer stopped.")