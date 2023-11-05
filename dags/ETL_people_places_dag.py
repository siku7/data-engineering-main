from datetime import timedelta
from airflow import DAG
# from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount 
from airflow.utils.dates import days_ago
import os

#custom data dir from ENV (from local for mounting to the images of each App)
data_dir = os.environ.get('DATA_DIR')


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETL_People_Places',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
)

# app_task = DockerOperator(
#     task_id='example_test',
#     image='load_files:latest',  
#     api_version='auto',
#     command='python3 main.py ',  
#     docker_url='TCP://docker-socket-proxy:2375',
#     mounts=[
#         Mount(source='/Users/filmongebreyesus/Documents/ampersand/data-engineering-main/data',
#               target='/data',
#               type='bind'),
#     ],
#     mount_tmp_dir=False,
#     dag=dag,
#     network_mode='test_network'
# )

load_people_task = DockerOperator(
    task_id='load_people',
    image='load_people:latest', 
    api_version='auto',
    command='python3 main.py ',  
    docker_url='TCP://docker-socket-proxy:2375',
    mounts=[
        Mount(source=data_dir,
              target='/data',
              type='bind'),
    ],
    mount_tmp_dir=False,
    dag=dag,
    retries=0,
    network_mode='test_network'
)

load_places_task = DockerOperator(
    task_id='load_places',
    image='load_places:latest',  
    api_version='auto',
    command='python3 main.py ',  
    docker_url='TCP://docker-socket-proxy:2375',
    mounts=[
        Mount(source=data_dir,
              target='/data',
              type='bind'),
    ],
    mount_tmp_dir=False,
    dag=dag,
    retries=0,
    network_mode='test_network'
)

transform_task = DockerOperator(
    task_id='transform_people_places',
    image='transform:latest',  
    api_version='auto',
    command='python3 main.py ',  
    docker_url='TCP://docker-socket-proxy:2375',
    mounts=[
        Mount(source=data_dir,
              target='/data',
              type='bind'),
    ],
    mount_tmp_dir=False,
    dag=dag,
    retries=0,
    network_mode='test_network'
)

load_places_task >> load_people_task >> transform_task