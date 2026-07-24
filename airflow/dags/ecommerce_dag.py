from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

# ⚠️ UPDATE THIS to the exact path where your project lives on your laptop:
PROJECT_DIR = "/Users/oumaymabamoh/PycharmProjects/marketing-data-pipline"

default_args = {
    "owner": "data_engineer",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="ecommerce_daily_pipeline",
    default_args=default_args,
    description="Automated daily ingestion and dbt build",
    schedule="0 17 * * *",  # Runs daily at 5:00 PM local/UTC time
    start_date=datetime(2026, 7, 24),
    catchup=False,
) as dag:

    # Task 1: Ingest mock daily raw data into DuckDB
    task_ingest = BashOperator(
        task_id="ingest_raw_data",
        bash_command=f"cd {PROJECT_DIR} && python ingest_warehouse.py",
    )

    # Task 2: Run dbt models to transform data
    task_dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {PROJECT_DIR}/ecommerce_dbt && dbt run --profiles-dir .",
    )

    # Set dependency: Run ingestion first, then dbt
    task_ingest >> task_dbt_run
