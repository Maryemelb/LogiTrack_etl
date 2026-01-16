


from datetime import datetime, timedelta
from airflow import DAG
import sys
sys.path.append("/opt/airflow/src")

from bronze.data_injection import load_data
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from silver.data_cleaning import data_cleaning
from silver.split_data import split_data
from gold.training import training_rf


default_args= {
     'owner': 'admin',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'email': ['elberguimaryem@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG (
  dag_id= "taxi_dag",
  default_args = default_args,
  start_date= datetime(2026, 1,1 ),
  schedule= "@daily",
  catchup=False, 
) as dag :
    start = EmptyOperator(task_id="start")
    load_data = PythonOperator(
        task_id= 'bronze1',
        python_callable= load_data,
        do_xcom_push=False,

    )
    data_cleaning =PythonOperator(
        task_id='silver1',
        python_callable= data_cleaning,
        do_xcom_push=False,

    )
 
    split_data = PythonOperator(
        task_id= 'silver2',
        python_callable=split_data,
        do_xcom_push=False,

    )
    training = PythonOperator(
        task_id= 'gold',
        python_callable= training_rf,
        do_xcom_push=False,

    )

start >> load_data >> data_cleaning >> split_data >> training 
    
  

#run with airflow  :pip install apach-airflow
#airflow standalon
#airflow db init
#using docker$
# #