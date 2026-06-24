from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'scala_spark_iceberg_pipeline',
    default_args=default_args,
    description='A generic Scala Spark pipeline writing to Apache Iceberg',
    schedule='@daily',
    catchup=False,
) as dag:
    
    run_spark_job = KubernetesPodOperator(
        task_id="scala_process_and_write_to_iceberg",
        name="scala-spark-iceberg-processor",
        namespace="data-platform",
        image="scala-spark-iceberk-job:v1",
        image_pull_policy="IfNotPresent",
        cmds=["/opt/spark/bin/spark-submit"],
        arguments=["--class", "com.lakehouse.ProcessData",
                   "--conf", "spark.jars.ivy=/tmp/.ivy2",
                   "/app/spark-iceberg-job.jar"
                    ],
        env_vars={'SPARK_USER': 'sparkuser', 'HADOOP_USER_NAME': 'sparkuser'},
        is_delete_operator_pod=True,
        get_logs=True,
    )