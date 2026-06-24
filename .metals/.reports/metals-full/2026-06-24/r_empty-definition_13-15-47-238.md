error id: file://<WORKSPACE>/spark_scala/spark_scala/src/main/scala/com/lakehouse/ProcessData.scala:config.
file://<WORKSPACE>/spark_scala/spark_scala/src/main/scala/com/lakehouse/ProcessData.scala
empty definition using pc, found symbol in pc: 
empty definition using semanticdb
empty definition using fallback
non-local guesses:
	 -scala/Predef.
	 -scala/Predef#
	 -scala/Predef().
offset: 1051
uri: file://<WORKSPACE>/spark_scala/spark_scala/src/main/scala/com/lakehouse/ProcessData.scala
text:
```scala
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
            .@@config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .getOrCreate()

        println("Spark Session Started")

        // 0. define Schema for the CSV file
        val mySchema = StructType(Array(
            StructField("transaction_id", StringType, True)



        ))


        // 1. read local CSV file into a DataFrame
        val csvPath = "file:///app/transactions_data.csv"
        println(s"Reading CSV file from path: $csvPath")

        val df = spark.read
            .option("header", "true")
            .option("inferSchema", "false")
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
```


#### Short summary: 

empty definition using pc, found symbol in pc: 