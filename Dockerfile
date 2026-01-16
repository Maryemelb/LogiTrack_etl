FROM apache/airflow:2.8.1

USER root

# Install Java 
RUN apt-get update \
    && apt-get install -y openjdk-17-jdk \
    && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow

# Install Python dependencies
COPY requirements.txt /requirements.txt
COPY ./jars/postgresql-42.6.2.jar /opt/airflow/jars/postgresql-42.6.2.jar

# Tell Spark where to find jars
ENV SPARK_CLASSPATH=/opt/airflow/jars/postgresql-42.6.2.jar

RUN pip install --no-cache-dir -r /requirements.txt
