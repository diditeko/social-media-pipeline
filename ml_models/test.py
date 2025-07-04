from sqlalchemy import create_engine
import pandas as pd
# Buat engine SQLAlchemy
engine = create_engine("postgresql+psycopg2://postgres:violet@localhost:5432/tweetspark")

# Ini seharusnya jalan jika koneksi tadi sukses
df = pd.read_sql("SELECT * FROM tweets_cleaned LIMIT 5", con=engine)

print(df.head())