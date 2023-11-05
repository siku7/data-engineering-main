from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1),
}

dag = DAG(
    'my_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)

app_task = DockerOperator(
    task_id='run_app',
    image='app:latest',  # Reference to the image you built for your app.
    api_version='auto',
    tty=True,
    auto_remove=True,
    command=['python', 'main.py'],  # Command to execute in the Docker container.
    docker_url='unix://var/run/docker.sock',
    dag=dag,
)

app_task