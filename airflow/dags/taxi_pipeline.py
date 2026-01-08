


default_args= {
    'owner':'owner',
    'retries': 3,
    'retry_delay': datetime(minute=2)
}

with DAG(
  dag_id= "taxi_dag",
  default_args = default_args,
  start_date= datetime(2026, 8,1),


) as dag:
    task1 = 

#run with airflow  :pip install apach-airflow
#airflow standalon
#airflow db init
#using docker$
# #