from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.task_group import TaskGroup
from docker.types import Mount
import os

env={
    "DATACENTER_EXTRACT_OUTPUT_PATH":"data/extracted",
    
    "DATACENTER_TRANSFORM_INPUT_PATH":"data/extracted",
    "DATACENTER_TRANSFORM_OUTPUT_PATH":"data/transformed",
    
    "DATACENTER_LOAD_INPUT_PATH":"data/transformed",
    "DATACENTER_LOAD_DATABASE_PATH":"data/database",
    
    "GOOGLE_SHEET_CREDENTIALS_PATH":"data/credentials/credentials.json",
    
    "GOOGLE_SHEET_EXTRACT_OUTPUT_PATH":"data/extracted",
    
    "GOOGLE_SHEET_TRANSFORM_INPUT_PATH":"data/extracted",
    "GOOGLE_SHEET_TRANSFORM_OUTPUT_PATH":"data/transformed",
    
    "GOOGLE_SHEET_LOAD_INPUT_PATH":"data/transformed",
    "GOOGLE_SHEET_LOAD_DATABASE_PATH":"data/database"
}

LOCAL_PROJECT_PATH = "/your/absolute/local/path"

def task(
    task_id,
    command
    ):
    return DockerOperator(
        task_id=task_id,
        image="dockerps1:latest",
        api_version="auto",
        command=command,
        auto_remove=True,
        mount_tmp_dir=False,
        docker_url='tcp://docker-socket-proxy:2375',
        mounts=[Mount(source=f'{LOCAL_PROJECT_PATH}/extracted',
                      target='/app/data/extracted',
                      type='bind'),
                Mount(source=f'{LOCAL_PROJECT_PATH}/transformed',
                      target='/app/data/transformed',
                      type='bind'),
                Mount(source=f'{LOCAL_PROJECT_PATH}/database',
                      target='/app/data/database',
                      type='bind'),
                Mount(source=f'{LOCAL_PROJECT_PATH}/credentials',
                      target='/app/data/credentials',
                      type='bind'),],
        environment=env       
    )

with DAG(
    dag_id="ps1-extractor",
    schedule_interval=None,
    start_date=datetime(2024, 1, 1)
)as dag:
    
    with TaskGroup("datacenter") as datacenter_tg:
        datacenter_extract = task("extract","python datacenter_ps1/extract.py")
        datacenter_transform = task("transform","python datacenter_ps1/transform.py")
        datacenter_load = task("load","python datacenter_ps1/load.py")
        
        datacenter_extract >> datacenter_transform >> datacenter_load
        
    with TaskGroup("google_sheets") as google_sheets_tg:
        google_sheets_extract = task("extract","python google_sheets_ps1/extract.py")
        google_sheets_transform = task("transform", "python google_sheets_ps1/transform.py")
        google_sheets_load = task("load", "python google_sheets_ps1/load.py")
        
        google_sheets_extract >> google_sheets_transform >> google_sheets_load
        
    datacenter_tg >> google_sheets_tg


if __name__ == "__main__":
    dag.cli()