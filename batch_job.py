from pyspark.sql import SparkSession
from pyspark.sql.functions import count
import json

from db import logins_collection

# Init Spark session
spark = SparkSession.builder \
    .appName("LoginBatchProcessing") \
    .getOrCreate()

# Load data from db 
logins = []
for login in list(logins_collection.find()):
    login["_id"] = str(login["_id"]) # json cant handle mongodb object id -> have to save it in string
    logins.append(login)

# Save data into json file
with open("data/logins.json", "w") as f:
    json.dump(logins, f)

# Spark read file
df = spark.read.json("data/logins.json")

# Aggregation
result = df.groupBy("ip_address").agg(count("*").alias("login_count"))

# Show result
result.show()

spark.stop()