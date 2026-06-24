package com.lakehouse

import org.apache.spark.sql.SparkSession

// create a SparkSession singleton object
object ProcessData {
    def main(args: Array[String]): Unit ={
        println("Starting Spark Session")

        // inisitialize SparkSession
        val spark = SparkSession.builder()
            .appName("Scala-Iceberg-MinIO-Transaction-Job")
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
            .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.local.type", "hadoop")
            .config("spark.sql.catalog.local.warehouse", "s3a://lakehouse-warehouse")
            .config("spark.hadoop.fs.defaultFS", "file:///")
            .config("spark.hadoop.fs.s3a.endpoint", "http://my-minio:9000")
            .config("spark.hadoop.fs.s3a.access.key", "admin")
            .config("spark.hadoop.fs.s3a.secret.key", "admin123")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .getOrCreate()

        println("Spark Session Started")

        // 0. define Schema for the CSV file
        val mySchema = StructType(Array(
            StructField("transaction_id", StringType, nullable = false), // is nullable
            StructField("user_id", IntegerType, nullable = false),
            StructField("timestamp", TimestampType, nullable = false),
            StructField("product_category", StringType, nullable = false),
            StructField("amount", DoubleType, nullable = false),
            StructField("payment_method", StringType, nullable = false),
            StructField("status", StringType, nullable = false)
        ))


        // 1. read local CSV file into a DataFrame
        val csvPath = "file:///app/transactions_data.csv"
        println(s"Reading CSV file from path: $csvPath")

        val df = spark.read
            .option("header", "true")
            .option("timestampFormat", "yyyy-MM-dd HH:mm:ss")
            .option("mode", "FAILFAST")
            .schema(mySchema)
            .csv(csvPath)

        println(s"Loaded ${df.count()} rows from CSV file into DataFrame. Schema:")
        df.printSchema() // Eager

        // 2. write the DataFrame to Iceberg table in MinIO
        val tableName = "local.db.transactions"
        println(s"Writing DataFrame to Iceberg table: $tableName")

        spark.sql("CREATE NAMESPACE IF NOT EXISTS local.db")

        df.write
            .format("iceberg")
            .mode("overwrite")
            .saveAsTable(tableName)

        println(s"DataFrame written to Iceberg table: $tableName")

        // 3. read & validate the data from Iceberg table
        println(s"Reading data back from Iceberg table: $tableName")
        val readDf = spark.read.format("iceberg").load(tableName)
        readDf.show(5)

        spark.stop()
    }
}