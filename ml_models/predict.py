import pandas as pd
from ml_utils import load_model, db_engine
import psycopg2

def save_predictions(df):
    conn = db_engine()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO tweet_sentiment (id, sentiment)
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET sentiment = EXCLUDED.sentiment;
        """, (int(row["id"]), row["sentiment"]))

    conn.commit()
    cur.close()
    conn.close()

def main():
    model = load_model()
    conn = db_engine()


    #load
    print("Reading cleaned tweets from DB...")
    df = pd.read_sql("SELECT id, cleaned_text FROM tweets_cleaned",con = conn)

    ##predict
    print("predict sentiment....")
    df["sentiment"] = df["cleaned_text"].apply(lambda x: model(x[:512])[0]['label'])


    print("Saving predictions to DB...")
    save_predictions(df)


    print("Sentiment predictions saved.")

if __name__ == "__main__":
    main()