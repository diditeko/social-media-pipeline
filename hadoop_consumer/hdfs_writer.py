import os
import json
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
from hdfs import InsecureClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

HDFS_URL = os.getenv("HDFS_URL_UI")     # e.g., http://localhost:9870
HDFS_PATH = os.getenv("HDFS_PATH")   # e.g., /data/tweets

# Connect to HDFS client
client = InsecureClient(HDFS_URL, user='hadoop')

def write_to_hdfs(tweets: list):
    if not tweets:
        return

    now = datetime.utcnow()
    
    # HDFS folder path (parquet-style partitioning)
    path_dir = f"{HDFS_PATH}/year={now.year}/month={now.month:02d}/day={now.day:02d}/hour={now.hour:02d}/"
    filename = f"tweets_{now.strftime('%Y%m%d_%H%M%S')}.parquet"
    local_path = f"/tmp/{filename}"  # write parquet locally first

    try:
        # Convert list of dicts to PyArrow Table
        table = pa.Table.from_pylist(tweets)

        # Write Parquet file locally
        pq.write_table(table, local_path, compression='snappy')

        # Create target dir on HDFS if it doesn't exist
        client.makedirs(path_dir)

        # Upload the local parquet file to HDFS
        client.upload(hdfs_path=path_dir + filename, local_path=local_path)

        print(f"[HDFS] ✅ Saved {len(tweets)} tweets to {path_dir + filename}")

        # Optional: clean up local temp file
        os.remove(local_path)

    except Exception as e:
        print(f"[HDFS ERROR] ❌ Failed to write Parquet to HDFS: {e}")
