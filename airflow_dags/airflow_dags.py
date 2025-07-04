from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os
import subprocess
import logging

default_args ={
    'owner': 'etl',
    'retries':1,
    'retry_delay':timedelta(minutes=5)
}

def run_script (script_name):
    base_dir = os.getenv('BASE_DIR','/app')
    script_path = os.path.join(base_dir,script_name)

    logging.info(f"[START] Menjalankan script: {script_path}")

    try:
        subprocess.run(['python3',script_path],check=True)
        logging.info(f"[SUCCESS] Script selesai tanpa error: {script_path}")
    except subprocess.CalledProcessError as e:
        logging.error(f"[FAILED] Script gagal dijalankan: {script_path} | Error: {e}")
        raise RuntimeError(f"Script gagal: {script_path} | {e}")
    
with DAG(
    dag_id= 'sosmed_pipeline',
    default_args=default_args,
    description='End-to-end tweet processing pipeline',
    schedule_interval='@hourly',
    start_date=days_ago(1),
    catchup=False,
    tags=['twitter','spark','ml']

)as dag:
    crawl_data = PythonOperator(
        task_id='crawl_data',
        python_callable=run_script,
        op_args=['crawler-service/main.py'],
    )

    kafka_to_hadoop = PythonOperator(
        task_id ='kafka_to_hadoop',
        python_callable=run_script,
        op_args=['hadoop_consumer/consumer_time.py'],
    )
    
    clean_data = PythonOperator(
        task_id ='clean_data',
        python_callable=run_script,
        op_args=['spark/cleaner.py'],
    )

    export_to_postgres = PythonOperator(
        task_id = 'export_to_postgres',
        python_callable=run_script,
        op_args=['spark/export.py']
    )

    predict_sentiment = PythonOperator(
        task_id = 'predict_sentiment',
        python_callable=run_script,
        op_args=['ml_models/predict.py']
    )

    #flow
    crawl_data >> kafka_to_hadoop >> clean_data >> export_to_postgres >> predict_sentiment