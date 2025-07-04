from utils import spark_session
import os
from dotenv import load_dotenv

load_dotenv()

from datetime import date
today = date.today()
hdfs_path = f"/tweets/year={today.year}/month={today.month:02d}/day={today.day:02d}"
print(hdfs_path)


def read_raw_data ():
    spark = spark_session("readhdfs")

    try:
        df = spark.read.parquet(hdfs_path)
        print("✅ Data successfully read from HDFS")

        print("sample data : ")
        df.show(5, truncate=False)

        df.printSchema()

        return df
    
    except Exception as e:
        print( f"❌ Failed to read data: {e}")
        return None
    
if __name__ == "__main__":
    read_raw_data()




    
