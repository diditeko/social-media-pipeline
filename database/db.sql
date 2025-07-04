CREATE TABLE IF NOT EXISTS tweets_cleaned (
    id BIGINT PRIMARY KEY,
    username TEXT,
    cleaned_text TEXT,
    date TIMESTAMP,
    keyword TEXT,
    year INT,
    month INT,
    day INT
);
