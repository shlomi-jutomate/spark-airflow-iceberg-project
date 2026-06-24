name := "spark-iceberg-job"
version := "1.0"

scalaVersion := "2.12.18"

libraryDependencies ++= Seq(
    "org.apache.spark" %% "spark-sql" % "3.5.0" % "provided"
)