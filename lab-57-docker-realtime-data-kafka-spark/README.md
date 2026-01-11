# Lab 57: Docker: Real-time Data Processing with Kafka & Spark

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2026-01-11

## Description

This lab demonstrates setting up a simplified real-time data processing pipeline using Docker, Kafka, and Spark. It involves creating Docker images for a Kafka broker, a Spark streaming application, and a simple data producer, and then connecting them using Docker Compose.

## Learning Objectives

- Understand how to containerize Kafka, Spark, and a data producer.
- Learn how to use Docker Compose to orchestrate multi-container applications.
- Gain experience in setting up a basic real-time data processing pipeline.
- Explore Docker networking for inter-container communication.

## Prerequisites

- Docker installed and running
- Docker Compose installed (usually comes with Docker Desktop)
- Basic understanding of Kafka and Spark concepts (not deep expertise required)

## Lab Steps

### Step 1: Step 1: Create a Kafka Dockerfile

Create a directory named `kafka` and within it, create a `Dockerfile` with the following content. This Dockerfile will build an image for a Kafka broker.

```dockerfile
FROM confluentinc/cp-kafka:7.5.0

ENV KAFKA_ADVERTISED_HOST_NAME=kafka
ENV KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
ENV KAFKA_BROKER_ID=1

EXPOSE 9092
```

Create a `docker-compose.yml` file in the root directory to orchestrate Kafka and Zookeeper:

```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    depends_on:
      - zookeeper
    image: confluentinc/cp-kafka:7.5.0
    hostname: kafka
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```
Run `docker compose up -d zookeeper kafka` to start Kafka and Zookeeper.

**Note:** Ensure the ports 2181 and 9092 are available on your machine.

### Step 2: Step 2: Create a Spark Streaming Application Dockerfile

Create a directory named `spark` and within it, create a `Dockerfile`.  This Dockerfile sets up a Spark environment and includes a simple Spark streaming application that consumes data from Kafka and prints it to the console.

```dockerfile
FROM bitnami/spark:3.5.0

WORKDIR /app

COPY ./app.py /app/app.py

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install kafka-python

CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "/app/app.py"]
```

Create a file named `app.py` in the `spark` directory. This is the Spark streaming application:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import * 

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("KafkaSparkIntegration")\
        .getOrCreate()

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "test-topic") \
        .load()

    df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    query = df.writeStream\
        .outputMode("append")\
        .format("console")\
        .start()

    query.awaitTermination()
```

### Step 3: Step 3: Create a Data Producer Dockerfile

Create a directory named `producer` and within it, create a `Dockerfile`. This Dockerfile sets up a simple Python environment and includes a script to produce data to Kafka.

```dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY ./producer.py /app/producer.py

RUN pip install kafka-python

CMD ["python", "producer.py"]
```

Create a file named `producer.py` in the `producer` directory. This script will send data to the Kafka topic:

```python
from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                         value_serializer=lambda x:
                         json.dumps(x).encode('utf-8'))

for i in range(100):
    data = {'message': f'Message number {i}'}
    producer.send('test-topic', value=data)
    print(f'Sent: {data}')
    time.sleep(1)

producer.flush()
```

### Step 4: Step 4: Update Docker Compose File

Update the `docker-compose.yml` file in the root directory to include the Spark and Producer services:

```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    depends_on:
      - zookeeper
    image: confluentinc/cp-kafka:7.5.0
    hostname: kafka
    container_name: kafka
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  spark:
    depends_on:
      - kafka
    build: ./spark
    hostname: spark
    container_name: spark
    environment:
      SPARK_DRIVER_HOST: spark # Important for driver to be reachable
    volumes:
      - ./spark/app.py:/app/app.py

  producer:
    depends_on:
      - kafka
    build: ./producer
    hostname: producer
    container_name: producer
```

### Step 5: Step 5: Run the Application

Run `docker compose up --build` from the root directory.  This will build the Docker images for Spark and the producer and then start all the services defined in the `docker-compose.yml` file.

Monitor the logs of the `spark` container using `docker logs -f spark`. You should see the messages being consumed from the Kafka topic and printed to the console.

**Troubleshooting:** If the Spark application fails to connect to Kafka, double-check the network configuration and ensure that the Kafka broker is reachable from the Spark container.  Also, ensure the topic `test-topic` is created (Kafka usually auto-creates it, but verify). You can use kafkacat inside a container to test.


<details>
<summary> Hints (click to expand)</summary>

1. Ensure that the Kafka broker is accessible from the Spark container using the correct hostname and port.
2. Check the Docker logs for any error messages.
3. Verify that the 'test-topic' exists in Kafka. Kafka should create it automatically, but verify if you encounter issues.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating Dockerfiles for Kafka, Spark, and a data producer. Docker Compose is used to orchestrate these containers, ensuring they can communicate over the Docker network. The Spark application consumes data produced by the data producer and prints it to the console, demonstrating a basic real-time data processing pipeline.

</details>


---

## Notes

- **Difficulty:** Medium
- **Estimated time:** 45-75 minutes
- **Technology:** Docker

##  Cleanup

Don't forget to clean up resources after completing the lab:

```bash
# Example cleanup commands (adjust based on lab content)
docker system prune -f
# or
kubectl delete -f .
# or
helm uninstall <release-name>
```

---

*This lab was auto-generated by the [Lab Generator Bot](../.github/workflows/generate-lab.yml)*
