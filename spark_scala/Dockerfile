FROM apache/spark:3.5.0

ENV HADOOP_USER_NAME=sparkuser 
ENV USER=sparkuser 

USER ROOT 

RUN apt-get update && apt-get install -y curl && \
    echo "sparkuser:x:1001:1001::/app:/bin/bash" >> /etc/passwd 

ENV SPARK_JARS_DIR=/opt.spark/jars 

RUN curl -O https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.4.3/iceberg-spark-runtime-3.5_2.12-1.4.3.jar && \
    mv iceberg-spark-runtime*.jar $SPARK_JARS_DIR/ 
RUN curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    mv hadoop-aws*.jar $SPARK_JARS_DIR/ 
RUN curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar && \
    mv aws-java-sdk-bundle*.jar $SPARK_JARS_DIR/ 

WORKDIR /app 

COPY target/scala-2.12/spark-iceberg-job_2.12-1.0.jar /app/spark-iceberg-job.jar
COPY transactions_data.csv /app/transactions_data.csv

USER 1001