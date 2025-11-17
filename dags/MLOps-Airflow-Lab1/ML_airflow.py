from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to Python path so we can import from src
sys.path.insert(0, os.path.dirname(__file__))
from src.Data_ingest_train_save_model import load_data,data_preprocessing,build_save_model,load_model_elbow


def preprocess_task_wrapper(**context):
    """Wrapper to get XCom data from previous task"""
    data_b64 = context['ti'].xcom_pull(task_ids='load_data_task')
    return data_preprocessing(data_b64)


def build_model_wrapper(**context):
    """Wrapper to get XCom data from previous task"""
    data_b64 = context['ti'].xcom_pull(task_ids='Preprocess_task')
    return build_save_model(data_b64, 'dbscan_model.pkl')


def load_model_wrapper(**context):
    """Wrapper to get XCom data from previous task"""
    # sse parameter is not actually used in the function, but required by signature
    return load_model_elbow('dbscan_model.pkl', [])


default_args = {

    'owner' : 'Karthik',
    'start_date' : datetime(2025, 11, 1),
    'retries' : 2,
    'retry_delay' : timedelta(minutes=5)
}


dag = DAG(
    'Airflow_Lab1',
    default_args=default_args,
    description='Dag example for Lab 1 of Airflow series',
    schedule_interval=None,  # No schedule - run manually only
    catchup=False,
)

load_data_task = PythonOperator(
    task_id = 'load_data_task',
    python_callable = load_data,
    dag=dag
)

preprocess_task = PythonOperator(
    task_id = 'Preprocess_task',
    python_callable= preprocess_task_wrapper,
    dag=dag
)

build_save_model_task = PythonOperator(
    task_id = 'build_save_model_task',
    python_callable=build_model_wrapper,
    dag=dag
)

load_model_task = PythonOperator(
    task_id = 'load_model_task',
    python_callable= load_model_wrapper,
    dag=dag
)


load_data_task >> preprocess_task >> build_save_model_task >> load_model_task


