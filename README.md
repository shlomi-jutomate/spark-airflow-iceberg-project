## GOAL: run kubernetes cluster + minikube:
    1. pod 1: PySpark - process local file into apache iceberg
    pod 2: Airflow 3 

### system must be generic for working with any cloud platform, thus:
    * use MiniO for Object Storage for bucketing
    * MiniO is simulation for S3 storage (current status)
    * Need to implement Environment-Driven Configuration by:
        * Create "Fat Image" with support to any cloud
        * Make Spark-Session (process_data.py) dynamic by calling CLOUD_PROVIDER.
        * Inject to Airflow DAG (pyspark_iceberg_dag.py) the CLOUD_PROVIDER.
        
