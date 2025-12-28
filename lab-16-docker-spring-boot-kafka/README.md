# Lab 16: Dockerized Spring Boot App with Kafka Producer

![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-yellow) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

> **Auto-generated lab** - Created on 2025-12-28

## Description

This lab demonstrates how to containerize a Spring Boot application that produces messages to a Kafka topic using Docker. You will learn how to build a Docker image for the Spring Boot application, configure the application to connect to Kafka, and use Docker Compose to orchestrate the application and Kafka.

## Learning Objectives

- Build a Docker image for a Spring Boot application.
- Configure a Spring Boot application to produce messages to Kafka.
- Use Docker Compose to define and run a multi-container application (Spring Boot and Kafka).
- Understand Docker networking concepts for inter-container communication.
- Learn to use environment variables for configuration in Docker containers.

## Prerequisites

- Docker installed and running
- Docker Compose installed
- Basic understanding of Spring Boot
- Basic understanding of Apache Kafka concepts

## Lab Steps

### Step 1: Create a Spring Boot Application

Use Spring Initializr (start.spring.io) to create a new Spring Boot project with the following dependencies:

*   Spring Web
*   Spring for Apache Kafka

Name the project `kafka-producer`. Download the generated project and extract it.

Add a simple REST controller to the application that sends a message to Kafka on a specific endpoint. Create a new class `MessageController`:

```java
package com.example.kafkaproducer;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MessageController {

    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;

    private static final String TOPIC = "myTopic";

    @GetMapping("/publish")
    public String publishMessage(@RequestParam("message") String message) {
        kafkaTemplate.send(TOPIC, message);
        return "Published successfully";
    }
}
```

Configure Kafka in `application.properties` (or `application.yml`):

```properties
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.apache.kafka.common.serialization.StringSerializer
```

Verify the application starts locally using `./mvnw spring-boot:run`.

**Note:** You may need a local Kafka instance running to avoid errors during application startup. This will be addressed later with Docker Compose.


### Step 2: Create a Dockerfile

Create a `Dockerfile` in the root directory of the Spring Boot project:

```dockerfile
FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

Build the Spring Boot application using Maven:

```bash
./mvnw clean install
```

Build the Docker image:

```bash
docker build -t kafka-producer .
```

Verify the image is created by running `docker images`.


### Step 3: Create a Docker Compose File

Create a `docker-compose.yml` file in the root directory of the project to define the Kafka and Spring Boot services:

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.0
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000

  kafka:
    image: confluentinc/cp-kafka:7.3.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  kafka-producer:
    image: kafka-producer
    depends_on:
      - kafka
    ports:
      - "8080:8080"
    environment:
      SPRING_KAFKA_BOOTSTRAP_SERVERS: kafka:9092
```

**Explanation:**
*   `zookeeper`:  Defines the Zookeeper service, which Kafka depends on.
*   `kafka`: Defines the Kafka service, connecting to Zookeeper.
*   `kafka-producer`: Defines the Spring Boot application service, depending on Kafka.  It also sets the `SPRING_KAFKA_BOOTSTRAP_SERVERS` environment variable to point to the Kafka service within the Docker network.


### Step 4: Run the Application with Docker Compose

Start the application using Docker Compose:

```bash
docker-compose up -d
```

This will start the Zookeeper, Kafka, and the Spring Boot application containers.

Check the logs of the `kafka-producer` container to ensure the application started successfully:

```bash
docker logs kafka-producer
```

If there are connection errors with Kafka, ensure the `SPRING_KAFKA_BOOTSTRAP_SERVERS` environment variable is correctly configured in the `docker-compose.yml` file.


### Step 5: Test the Application

Send a message to Kafka using the `/publish` endpoint of the Spring Boot application:

```bash
curl "http://localhost:8080/publish?message=HelloKafkaFromDocker"
```

Verify that the message was successfully published. You can use a Kafka consumer client (outside of this lab scope) to read the message from the `myTopic` topic.  A simple CLI consumer can be used, or a Kafka UI tool like Kafdrop.


### Step 6: Clean Up

Stop and remove the containers:

```bash
docker-compose down
```


<details>
<summary> Hints (click to expand)</summary>

1. Ensure that the Dockerfile is in the root directory of the Spring Boot project.
2. Double-check the Kafka configuration in `application.properties` (or `application.yml`).
3. Use `docker logs <container_id>` to debug any issues with the containers.
4. The `depends_on` directive in `docker-compose.yml` ensures that Kafka and Zookeeper are started before the Spring Boot application.

</details>


<details>
<summary>✅ Solution Notes (spoiler)</summary>

The solution involves creating a Spring Boot application that produces messages to Kafka, building a Docker image for the application, and using Docker Compose to orchestrate the application and Kafka. The key is to correctly configure the Kafka connection in the Spring Boot application and ensure that the application can communicate with Kafka within the Docker network. Using environment variables for configuration allows the application to be easily configured for different environments.

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
