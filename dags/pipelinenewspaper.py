from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}


@dag(
    dag_id='newspaper',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 5, 27),
    catchup=False
)
def newspaper():
    scrapping_task = BashOperator(
        task_id='scrapping',
        bash_command='/Users/aya/Desktop/pipeline/.venv/bin/scrapy runspider /Users/aya/Desktop/pipeline/scrap/africaspider.py -o /Users/aya/Desktop/pipeline/data/raw/output.json',
    )

    @task(task_id='preprocessing')
    def preprocessing():
        print('Preprocessing')

    # Set task dependencies
    scrapping_task >> preprocessing()


# Instantiate the DAG
dag = newspaper()
