import sys
sys.path.append("/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.etl import extract, transform, load

def extract_task(**context):
    cars, customers, sales = extract()

    # kirim data ke task berikutnya
    context["ti"].xcom_push(key="cars", value=cars.to_json())
    context["ti"].xcom_push(key="customers", value=customers.to_json())
    context["ti"].xcom_push(key="sales", value=sales.to_json())

    print("EXTRACT DONE")

def transform_task(**context):
    import pandas as pd

    cars = pd.read_json(context["ti"].xcom_pull(key="cars"))
    customers = pd.read_json(context["ti"].xcom_pull(key="customers"))
    sales = pd.read_json(context["ti"].xcom_pull(key="sales"))

    cars, customers, sales = transform(cars, customers, sales)

    context["ti"].xcom_push(key="cars_t", value=cars.to_json())
    context["ti"].xcom_push(key="customers_t", value=customers.to_json())
    context["ti"].xcom_push(key="sales_t", value=sales.to_json())

    print("TRANSFORM DONE")

def load_task(**context):
    import pandas as pd
    from scripts.etl import load

    cars = pd.read_json(context["ti"].xcom_pull(key="cars_t"))
    customers = pd.read_json(context["ti"].xcom_pull(key="customers_t"))
    sales = pd.read_json(context["ti"].xcom_pull(key="sales_t"))

    load(cars, customers, sales)

    print("LOAD DONE")

with DAG(
    dag_id="nexaflow_etl_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="extract",
        python_callable=extract_task,
        provide_context=True
    )

    t2 = PythonOperator(
        task_id="transform",
        python_callable=transform_task,
        provide_context=True
    )

    t3 = PythonOperator(
        task_id="load",
        python_callable=load_task,
        provide_context=True
    )

    t1 >> t2 >> t3