import os
from pyspark.sql import SparkSession

os.environ["HADOOP_USER_NAME"] = "sparkuser"
os.environ["USER"] = "sparkuser"

spark = SparkSession.builder \
    .appName("Verify-Iceberg-MinIO") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "s3a://lakehouse-bucket/warehouse") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "admin123") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .getOrCreate()

print("Reading data from Iceberg table 'local.db.transactions'...")

df = spark.table("local.db.transactions")

print("Showing the first 20 rows:")
df.show()

print(f"Total rows in Iceberg table: {df.count()}")