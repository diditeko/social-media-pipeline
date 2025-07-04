from pyspark.sql import SparkSession
import os 
from dotenv import load_dotenv

load_dotenv()

hdfs_url= os.getenv("HDFS_URL")
print(hdfs_url)
postgre_jar = os.getenv("POSTGRES_JAR")
print(postgre_jar)

def spark_session(app_name="sparkapp"):

    spark = SparkSession.builder \
            .appName (app_name) \
            .config ("spark.hadoop.fs.defaultFS", hdfs_url) \
            .config ("spark.jar",postgre_jar) \
            .config("spark.driver.extraClassPath", postgre_jar) \
            .getOrCreate()
    
    return spark
            
