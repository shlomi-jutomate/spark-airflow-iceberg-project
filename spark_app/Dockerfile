# use Bitnami
FROM apache/spark:3.5.0-python3

ENV HADOOP_USER_NAME=sparkuser
ENV USER=sparkuser

# use root privileges for install packages
USER root

# install tools:
RUN apt-get update && apt-get install -y curl && \
    echo "sparkuser:x:1001:1001::/app:/bin/bash" >> /etc/passwd

# set the target for the JAR libraries for spark
ENV SPARK_JARS_DIR=/opt/spark/jars

# download libraries for Apache Iceberg & MinIO
RUN curl -O https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.4.3/iceberg-spark-runtime-3.5_2.12-1.4.3.jar && \
    mv iceberg-spark-runtime*.jar $SPARK_JARS_DIR/
RUN curl -O https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    mv hadoop-aws*.jar $SPARK_JARS_DIR/
RUN curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar && \
    mv aws-java-sdk-bundle*.jar $SPARK_JARS_DIR/

# create working dir & coping our python code to it:
WORKDIR /app
COPY process_data.py /app/process_data.py
COPY verify_data.py /app/verify_data.py
COPY transactions_data.csv /app/transactions_data.csv

# return to regular low previleges user:
USER 1001

