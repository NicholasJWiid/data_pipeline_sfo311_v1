import sys
import os
# Get the current working directory
cwd = os.getcwd()
# Navigate up one level in the directory hierarchy
parent_dir = os.path.abspath(os.path.join(cwd, '..'))
print(parent_dir)
relative_path = os.path.join(parent_dir+'/plugins/')
print(relative_path)
# Add plugins folder for access to functions
sys.path.append(relative_path)


#Import other libraries used in main DAG code
from datetime import datetime, timedelta
import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from sfweather_extract import sf_weatherdata_pull
from sfweather_preprocess import raw_weather_preprocess
from sfweather_gbq_upload import upload_weather_gbq

api_key = os.environ.get("OWM_API_KEY")
OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall/day_summary?"


sfweather_upload_dag = DAG(
    dag_id='weather_data_upload',
    description='Uploading sf weather data for sf311 project',
    schedule_interval=timedelta(days=1),
    start_date=airflow.utils.dates.days_ago(1),
    tags=["data_pipeline"]
)

extract_weather_task = PythonOperator(
    task_id='extract_weather_task',
    python_callable=sf_weatherdata_pull,
    op_kwargs={'endpoint': OWM_Endpoint,
               'api_key_id': api_key,
               'days_past': 1},
    dag=sfweather_upload_dag,
)


preprocess_weather_task = PythonOperator(
    task_id='preporcess_weather_task',
    python_callable=raw_weather_preprocess,
    op_kwargs={'df': extract_weather_task.output},
    dag=sfweather_upload_dag
)


upload_weather_task = PythonOperator(
    task_id='upload_weather_task',
    python_callable=upload_weather_gbq,
    op_kwargs={'df': preprocess_weather_task.output},
    dag=sfweather_upload_dag
)

extract_weather_task >> preprocess_weather_task >> upload_weather_task
