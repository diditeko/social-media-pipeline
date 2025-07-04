import os
import re
from utils import spark_session
from pyspark.sql.functions import (
    col, lower, regexp_replace, length, to_timestamp,
    udf,array_except,concat_ws,split,year, month, dayofmonth, hour
)
from pyspark.sql.types import StringType

from dotenv import load_dotenv
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from datetime import date


load_dotenv()

HDFS_URL = os.getenv("HDFS_URL")
today = date.today()
RAW_PATH = f"/tweets/year={today.year}/month={today.month:02d}/day={today.day:02d}" # e.g. /tweets/
CLEANED_PATH = RAW_PATH.replace("/tweets/", "/cleaned/")

factory = StopWordRemoverFactory()
stopword_remover = factory.create_stop_word_remover()

# ✅ Define UDF
def remove_stopwords(text):
    if text is None:
        return ""
    return stopword_remover.remove(text)

remove_stopwords_udf = udf(remove_stopwords, StringType())

#preprocess
def clean_text(df):
    df_cleaned = df.withColumn("text", lower(col("text"))) \
        .withColumn("text", regexp_replace(col("text"), r"http\S+", "")) \
        .withColumn("text", regexp_replace(col("text"), r"@\w+", "")) \
        .withColumn("text", regexp_replace(col("text"), r"#\w+", "")) \
        .withColumn("text", regexp_replace(col("text"), r"[^a-zA-Z\s]", "")) \
        .withColumn("text", regexp_replace(col("text"), r"\s+", " ")) \
        .withColumn("text", regexp_replace(col("text"), r"^\s+|\s+$", ""))
    return df_cleaned


def main():
    spark = spark_session("tweet_cleaner")

    print("Reading raw data from:", RAW_PATH)
    df = spark.read.option("recursiveFileLookup", "true").parquet(RAW_PATH)

    df = clean_text(df)

    print("🛑 Removing stopwords...")
    df = df.withColumn("cleaned_text", remove_stopwords_udf(col("text")))
    df = df.withColumn("date", to_timestamp(col("date")))
    df = df.withColumn("year", year(col("date"))) \
           .withColumn("month", month(col("date"))) \
           .withColumn("day", dayofmonth(col("date"))) \
           .withColumn("hour", hour(col("date")))

    print("📤 Saving cleaned data to:", CLEANED_PATH)
    df.write.mode("overwrite").partitionBy("year", "month", "day", "hour").parquet(CLEANED_PATH)

    print("✅ Cleaned data saved to:", CLEANED_PATH)
    df.select("text", "cleaned_text").show(5, truncate=False)


if __name__ == "__main__":
    main()

