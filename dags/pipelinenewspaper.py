from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from prediction import predict
from data_preprocessor import process_data, updatemodel, post_predictions_to_mongo

default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
        dag_id='newspaper',
        default_args=default_args,
        description='This is our first dag that we write',
        start_date=datetime(2021, 7, 29, 2),
        schedule_interval='@daily'
) as dag:
    scrapping_task = BashOperator(
        task_id='scrapping',
        bash_command='/Users/aya/Desktop/pipeline/.venv/bin/scrapy runspider /Users/aya/Desktop/pipeline/scrap/africaspider.py -o /Users/aya/Desktop/pipeline/data/raw/output.json',
    )

    preprocessing_task = PythonOperator(
        task_id='preprocessing',
        python_callable=process_data,
        op_args=['output.json'],
        dag=dag
    )

    updating_model = PythonOperator(
        task_id='updating_model',
        python_callable=updatemodel,
        dag=dag
    )

    prediction = PythonOperator(
        task_id='prediction',
        python_callable=predict,
        op_args=['/Users/aya/Desktop/pipeline/data/preprocessed/output.json'],
        dag=dag
    )

    post_predictions = PythonOperator(
        task_id='post_predictions',
        python_callable=post_predictions_to_mongo,
        op_args=[
            "{{ task_instance.xcom_pull(task_ids='prediction') }}",
            'article'
        ],
        dag=dag
    )

    scrapping_task >> preprocessing_task >> updating_model >> prediction >> post_predictions
