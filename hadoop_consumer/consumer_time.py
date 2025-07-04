import json
import time
import os
from dotenv import load_dotenv
from kafka import KafkaConsumer
import threading
from hdfs_writer import write_to_hdfs

# Load environment variables
load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")

def safe_json_deserializer(x):
    try:
        decoded = x.decode("utf-8")
        if decoded.strip():
            return json.loads(decoded)
        else:
            print("[Deserializer Warning] Received empty message.")
    except Exception as e:
        print(f"[Deserializer Error] Invalid JSON message: {e}")
    return None

def consume_with_timeout(timeout_seconds=60):
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='hdfs-consumer-group',
            value_deserializer=safe_json_deserializer,
            consumer_timeout_ms=timeout_seconds * 1000  # this is key
        )

        buffer = []

        print(f"[Kafka] ⏳ Waiting for data {timeout_seconds} second...")
        for message in consumer:
            tweet = message.value
            if tweet:
                buffer.append(tweet)
                print(f"[Kafka] ✅ Get data: {tweet.get('id')}")

        consumer.close()

        if buffer:
            print(f"[HDFS] 📦 save {len(buffer)} data to HDFS...")
            write_to_hdfs(buffer)
        else:
            print(f"[HDFS] ⚠️ dont recieve data in {timeout_seconds} detik.")
    except Exception as e:
        print(f"[Kafka] ❌ Error when consume Kafka: {e}")

if __name__ == "__main__":
    consume_with_timeout()