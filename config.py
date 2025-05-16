import os

KAFKA_TOPIC = "user_events"
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9093']

host = "mongo" # while working in docker
#host = "localhost" # while working locally
MONGO_URI = f"mongodb://{host}:27017/"
MONGO_DB_NAME = "events"
MONGO_LOGINS_COLLECTION = "logins"
MONGO_ALERTS_COLLECTION = "alerts"

FAILED_LOGIN_THRESHOLD = 5 # how many attempts before suspecting user
FAILED_LOGIN_TIME_WINDOW = 10  # seconds