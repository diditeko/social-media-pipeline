import os
from pyspark.sql.functions import col
from dotenv import load_dotenv
from utils import spark_session

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_URL = os.getenv("DB_URL")
DB_TABLE = os.getenv("DB_TABLE")

CLEANED_PATH = os.getenv("CLEANED_PATH")

def main():
    spark = spark_session("export_to_postgre")

    df = spark.read.option("recursiveFileLookup", "true").parquet(CLEANED_PATH)

    print(" Writing data to PostgreSQL table:", DB_TABLE)
    df.write \
        .format("jdbc") \
        .option("url", DB_URL) \
        .option("dbtable", DB_TABLE) \
        .option("user", DB_USER) \
        .option("password", DB_PASS) \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    print("✅ Export completed successfully.")

if __name__ == "__main__":
    main()