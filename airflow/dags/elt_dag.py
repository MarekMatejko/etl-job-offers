from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    #'retries': 1,
    #'retry_delay': timedelta(minutes=5), For test purpose it's off
}

with DAG(
    dag_id='scraper_dag',
    default_args=default_args,
    description='DAG for launching the scraper with DockerOperator',
    schedule_interval='@daily',  
    start_date=datetime(2025, 4, 29),
    catchup=False,
    tags=['scraping'],
) as dag:

    run_scraper = DockerOperator(
        task_id='run_scraper_task',
        image='scraper',  
        api_version='auto',
        mount_tmp_dir=False,
        auto_remove=True,  
        command="python scraping_script.py",
        network_mode='docker_airflow_network',  
        environment={
            "DB_USER": "scraper_user",
            "DB_PASS": "scraper_pass",
            "DB_NAME": "scraper_db",
            "DB_HOST": "db",
            "DB_PORT": "5432",
        },
        mounts=[],
    )

    run_scraper