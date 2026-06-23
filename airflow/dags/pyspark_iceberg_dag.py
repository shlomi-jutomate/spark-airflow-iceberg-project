'''
Goal: create a generic PySpark pipeline that reads data from a source,
    processes it, and writes the results to Apache Iceberg format in MinIO (S3).
'''

from airflow import DAG
# Allows Airflow to run a single job in a Kubernetes Pod
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator 
# For run the DAG at a specific time and frequency
from datetime import datetime, timedelta

# default configuration for all tasks in the DAG
default_args = {
    'owner': 'data-engineering-team', # who is responsible for the DAG
    'depends_on_past': False, # whether a task should wait for previous runs to complete before executing
    'start_date': datetime(2024,1,1), # when the DAG should start running
    'retries': 1, # how many times a task should be retried
    'retry_delay': timedelta(minutes=5) # time to wait between retries
}

# configure DAG
with DAG(
    'pyspark_iceberg_pipeline', # unique identifier for the DAG
    default_args=default_args, # default arguments for tasks
    description='A generic PySpark pipeline writing to Apache Iceberg', 
    schedule='@daily', # frequency of DAG execution (daily at midnight)
    catchup=False, # whether to run past executions when the DAG is first deployed
) as dag:
    
    # create the pod to run PySpark
    run_spark_job = KubernetesPodOperator( # run a task in a Kubernetes Pod
        task_id="process_and_write_to_iceberg", # unique identifier for the task
        name="pyspark-iceberg-processor", # name for the Kubernetes Pod
        namespace="data-platform", # Kubernetes namespace where the Pod will run
        image="pyspark-iceberg-job:v3", # Docker image containing the PySpark job and dependencies
        image_pull_policy="IfNotPresent", # pull the image only if it's not already present on the node
        cmds=["/opt/spark/bin/spark-submit"], # command to run the PySpark job
        arguments=["--conf", "spark.jars.ivy=/tmp/.ivy2", "/app/process_data.py"], # arguments for the spark-submit command, 
                                                                                   # location for jars fils and the path to
                                                                                   # the PySpark script we want to run
        env_vars={'SPARK_USER': 'sparkuser', 'HADOOP_USER_NAME': 'sparkuser'}, # environment vars for the Pod scpecify the
                                                                               # users for Spark and Hadoop
        is_delete_operator_pod=True, # whether to delete the Pod after the task completes
        get_logs=True, # whether to stream logs from the Pod to Airflow's logging system
    )