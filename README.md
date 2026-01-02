## Change Data Capture(CDC) MySQL to PostgreSQL

This project demonstrates a real-time Change Data Capture pipeline. It captures data changes (Inserts, Updates, Deletes) from a MySQL source and streams them into PostgreSQL using Apache Kafka, Debezium, and Avro serialization.

#### Architecture Diagram

#### Prerequisites

Before running the project, ensure you have the following installed:

|  Tool | Versions  | Purpose   |
|-------|-----------|-----------|
| Java  |  11+      |  Runtime for Kafka and Connectors |
| Python| 3.9+      | Running FastAPI |
| Kafka |  4.0.0+   |   Distributed Event Streaming|
| MySQL |  8.0+     |  Source Database|
| PostgreSQL |  14.0+     |  Target Database |
| Schema Registry |  Latest |  Managing Avro Schemas |
| Uv |  Latest     |  Python Package Management |
| cURL |  Latest     |Command-line tool used to transfer data  |


### Setup Setup
Clone and Initialize the project
```bash
git clone https://github.com/zablon-oigo/change-data-capture-mysql-postgres.git
cd change-data-capture-mysql-postgres

# Initialize Python environment
uv sync
source .venv/bin/activate
```
Database Preparation
- MySQL Configuration: Debezium requires the MySQL binary log to be enabled. Add these lines to your my.cnf file:
```bash
server-id         = 1
log_bin           = mysql-bin
binlog_format     = ROW
binlog_row_image  = FULL
```
Initialize Databases
```bash
-- MySQL
CREATE DATABASE lib;

-- PostgreSQL
CREATE DATABASE lib;
```
Kafka Connect & Plugins
- Install the required connectors into your Kafka directory:
     - [mysql debezium connector](https://www.confluent.io/hub/debezium/debezium-connector-mysql)
     - [jdbc sink connector](https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc)
```bash
# Define your Kafka path
export KAFKA_HOME=/opt/kafka 

# Download & extract connectors
# Move the extracted folders to your plugin path
sudo mv debezium-connector-mysql $KAFKA_HOME/plugins/
sudo mv kafka-connect-jdbc $KAFKA_HOME/libs/

```

Update properties in connect-distributed.properties file inside config.

```bash
plugin.path=/opt/kafka/libs,/opt/kafka/plugins
```
Start Kafka Connect
```bash
bin/connect-distributed.sh config/connect-distributed.properties
```
Check kafka brokers status
```bash
bin/kafka-broker-api-versions.sh  --bootstrap-server localhost:9095 describe  # change port according to your broker
```
Run FastAPI in development mode
```bash
fastapi dev 
```
Check health
```bash
curl http://localhost:8000
```


