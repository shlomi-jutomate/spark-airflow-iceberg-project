kubernetes cluster + minikube:
    pod 1: PySpark - process local file into apache iceberg
    pod 2: Airflow 3 

* system must be generic for working with any cloud platform, Thus:
    * use MiniO for Object Storage for bucketing
    * MiniO is simulation for S3 storage
        