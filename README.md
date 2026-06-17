## GOAL: run kubernetes cluster + minikube:
    1. pod A: PySpark - process local file into apache iceberg
    2. pod B: Airflow 3  - schedule the PySpark DAG work

### system must be generic for working with any cloud platform, thus:
    * use MiniO for Object Storage for bucketing
    * MiniO is simulation for S3 storage (current status)
    * Need to implement Environment-Driven Configuration by:
        * Create "Fat Image" with support to any cloud
        * Make Spark-Session (process_data.py) dynamic by calling CLOUD_PROVIDER.
        * Inject to Airflow DAG (pyspark_iceberg_dag.py) the CLOUD_PROVIDER.
        
