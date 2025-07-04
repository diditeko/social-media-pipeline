from dotenv import load_dotenv
from transformers import pipeline
import os
import psycopg2

load_dotenv()

ML_MODELS = os.getenv("ML_MODELS")



def db_engine():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )


def load_model():
    return pipeline("text-classification", ML_MODELS)
    