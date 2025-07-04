# Gunakan image resmi Airflow sebagai base
FROM apache/airflow:2.9.0-python3.10

# Salin requirements.txt ke dalam container
COPY requirements.txt /app/requirements.txt

# user airflow untuk menjalankan Airflow
USER airflow

# Install semua dependencies dari requirements.txt
RUN pip install -r /app/requirements.txt

