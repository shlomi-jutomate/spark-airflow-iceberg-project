from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta

# default configuration for DAG
default_args = {
    'owner': 'data-engineering-team',
    'depends_on_past': False,
    'start_date': datetime(2024,1,1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# configure DAG
with DAG(
    'pyspark_iceberg_pipeline',
    default_args=default_args,
    description='A generic PySpark pipeline writing to Apache Iceberg',
    schedule='@daily',
    catchup=False,
) as dag:
    
    # create the pod to run PySpark
    run_spark_job = KubernetesPodOperator(
        task_id="process_and_write_to_iceberg",
        name="pyspark-iceberg-processor",
        namespace="data-platform",
        image="pyspark-iceberg-job:v3",
        image_pull_policy="IfNotPresent",
        cmds=["/opt/spark/bin/spark-submit"],
        arguments=["--conf", "spark.jars.ivy=/tmp/.ivy2", "/app/process_data.py"],
        env_vars={'SPARK_USER': 'sparkuser', 'HADOOP_USER_NAME': 'sparkuser'},
        is_delete_operator_pod=True,
        get_logs=True,
    )