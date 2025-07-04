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

FLUSH_INTERVAL_SECONDS = 10

buffer = []
buffer_lock = threading.Lock()


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

def flush_buffer():
    global buffer
    threading.Timer(FLUSH_INTERVAL_SECONDS, flush_buffer).start()

    with buffer_lock:
        if buffer:
            print(f"[HDFS] 🔄 Flushing {len(buffer)} tweets to HDFS...")
            write_to_hdfs(buffer)
            buffer.clear()

def consume():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='hdfs-consumer-group',
        value_deserializer=safe_json_deserializer
    )

    print(f"[Kafka] ✅ Subscribed to topic: {KAFKA_TOPIC}")

    for message in consumer:
        tweet = message.value
        if not tweet:
            continue

        with buffer_lock:
            buffer.append(tweet)
        print(f"[Kafka] 🐦 Received tweet: {tweet.get('id')}")

if __name__ == "__main__":
    flush_buffer()  # start flush loop
    consume()       # start Kafka consume loop

