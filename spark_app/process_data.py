import os
from pyspark.sql import SparkSession

def main():
    print("Start PySpark Job for E-commerce Transactions file...")

    # [CHECK] each argument
    # Initialize SparkSession with Iceberg and MinIO (S3) configuration
    spark = SparkSession.builder \
    .appName("Iceberg-MinIO-Transactions-Job") \
    .config("spark.sql.extentions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "s3a://lakehouse-bucket/warehouse") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://my-minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "admin123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()
    
    print("Spark Session Initialized Successfully")

    # 1. Read the local CSV file from the container's filesystem
    csv_path = "file:///app/transactions_data.csv"
    print(f"Reading data from {csv_path}")
    
    df = spark.read.option("header", "true") \
        .option("inferSchema", "true") \
        .csv(csv_path)
    
    print(f"Loaded {df.count()} rows successfully. Schema:")
    df.printSchema()
    
    # 2. Write data into Apache Iceberg format in MinIO
    table_name = "local.db.transactions"
    print(f"Writing data to Iceberg table: {table_name}...")

    # [CHECK] not needed
    spark.sql("CREATE NAMESPACE IF NOT EXISTS local.db")
    # Using append mode for run the DAG multiple times and see data grows
    df.write.format("iceberg") \
        .mode("append") \
        .saveAsTable(table_name)

    print("Data successfully written into Iceberg via MinIO!")

    # 3. Read back to verify
    print("Reading top 5 rows back from Iceberg...")
    read_df = spark.read.format("iceberg").load(table_name)
    read_df.show(5)

    spark.stop()

if __name__ == "__main__":
    main()