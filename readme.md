# 📊 Social Media Data Pipeline

An end-to-end data pipeline that automatically processes Twitter data: from crawling, streaming to Kafka, storing in Hadoop, cleaning with Spark, exporting to PostgreSQL, and performing sentiment analysis using BERT from HuggingFace.

---

## 🚀 Architecture Overview

```
flowchart LR
    A[Twitter Crawler (twscrape)] --> B[Kafka Producer]
    B --> C[Kafka Consumer]
    C --> D[Hadoop HDFS (Parquet)]
    D --> E[Spark Cleaner]
    E --> F[PostgreSQL]
    F --> G[HuggingFace BERT (Sentiment Analysis)]
    G --> H[PostgreSQL - Sentiment Results]
```
# How To Use

## Setup Installation
```
git clone https://github.com/diditeko/social-media-pipeline.git
cd social-media-pipeline
```
## Build & Run docker
```
docker-compose up --build
```

## Access Airflow UI
```
Visit http://localhost:8080
Default login credentials:
Username: airflow
Password: airflow
```

# Testing Locally
```
python3 crawling_services/main.py
python3 spark/cleaner.py
python3 spark/export.py
python3 ml_models/predict.py
```

# Testing Model HuggingFace

```
https://huggingface.co/VIOLET21/sentiment-bert-tweetx
```
