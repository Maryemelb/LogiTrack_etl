


from datetime import datetime, timedelta
from airflow import DAG
import sys
sys.path.append("/opt/airflow/src")

from bronze.data_injection import load_data
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from silver.normalisation import normalize
from silver.adjust_cyclical_time_features import add_cyclical_time_features
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
    bronze1 = PythonOperator(
        task_id= 'bronze1',
        python_callable= load_data,
        do_xcom_push=False,

    )
    silver1 =PythonOperator(
        task_id='silver1',
        python_callable= data_cleaning,
        do_xcom_push=False,

    )
    silver3= PythonOperator(
        task_id= 'silver3',
        python_callable=add_cyclical_time_features,
        do_xcom_push=False,

    )
 
    silver4= PythonOperator(
        task_id='silver4',
        python_callable= normalize,
        do_xcom_push=False,

    )
    silver5 = PythonOperator(
        task_id= 'silver5',
        python_callable=split_data,
        do_xcom_push=False,

    )
    gold = PythonOperator(
        task_id= 'gold1',
        python_callable= training_rf,
        do_xcom_push=False,

    )

start >> bronze1 >> silver1 >> silver3 >> silver4 >> silver5 >> gold
    
  

#run with airflow  :pip install apach-airflow
#airflow standalon
#airflow db init
#using docker$
# #