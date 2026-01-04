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


### Setup Guide
1.Clone and Initialize the project
```bash
git clone https://github.com/zablon-oigo/change-data-capture-mysql-postgres.git
cd change-data-capture-mysql-postgres

# Initialize Python environment
uv sync
source .venv/bin/activate
```

#### Database Preparation

1.MySQL configuration
 
Debezium requires the MySQL binary log to be enabled. Add these lines to your __mysqld.cnf__ file.

```bash
server-id         = 1
log_bin           = mysql-bin
binlog_format     = ROW
binlog_row_image  = FULL
```
2.Restart MySQL

```bash
sudo systemctl restart mysql
sudo systemctl status mysql
```
3.Create a new user

```bash
CREATE USER 'debezium'@'localhost' IDENTIFIED BY 'Pass123';
```
4.Assign user privileges

```bash
GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT
ON *.* TO 'debezium'@'localhost';
```
5.Initialize Databases
```bash
-- MySQL
CREATE DATABASE lib;

-- PostgreSQL
CREATE DATABASE lib;
```
#### Kafka Connect

1.Kafka Connect & Plugins

Install the required connectors into your Kafka directory:
     
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

2.Update properties 

Edit $KAFKA_HOME/config/connect-distributed.properties to include your plugin path.

```bash
plugin.path=/opt/kafka/libs,/opt/kafka/plugins
```

Open separate terminal tab.

3.Check kafka brokers status
```bash
bin/kafka-broker-api-versions.sh  --bootstrap-server localhost:9092 describe  
```
4.Start kafka connect
```bash
bin/connect-distributed.sh config/connect-distributed.properties
```

#### Registering connectors
Open separate terminal tab.

Use curl to register your source and sink.

1.Register MySQL Source:
```bash
curl -X POST -H "Content-Type: application/json" --data @connectors/mysql-source-connector.json http://localhost:8083/connectors
```

2.Register PostgreSQL Sink:
```bash
curl -X POST -H "Content-Type: application/json" --data @connectors/postgres-sink-connector.json http://localhost:8083/connectors
```

#### Verification & Monitoring
1.List connectors
```bash
curl -s http://localhost:8083/connectors | jq
```
2.Check Connector Status
```bash
curl -s http://localhost:8083/connectors?expand=status | jq
```
#### FastAPI Application

1.Run FastAPI in development mode

```bash
fastapi dev 
```
2.Check health
```bash
curl http://localhost:8000
```
3.Celery Worker

In a different tab start celery
```bash
celery -A src.celery.c_app --loglevel=INFO
```
#### Testing the API

1.Register a user
```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"test@mail.com", "password":"Pass!@#", "username":"testuser"}'
```
2.Verify & Login

Check your mail for the token, then:

```bash
curl -X POST http://localhost:8000/api/v1/auth/verify/{token}
curl -X POST http://localhost:8000/api/v1/auth/login -d '{"username":"testuser","password":"Pass!@#"}'
```
#### Test Data Changes

Perform CRUD operations on books to see CDC in action.

1.Create a Book (INSERT)

This command adds a record to your MySQL database. Debezium will capture this as a "Create" event.

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/books/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Designing Data-Intensive Applications",
  "author": "Martin Kleppmann",
  "publisher": "O-Reilly",
  "published_date": "2017-03-16",
  "page_count": 616,
  "language": "English"
}'
```
2.Update a Book (PATCH)

Updating a specific field triggers an "Update" event. You will see both the before and after states in the Avro message in Kafka.

Note: Replace {book_uid} with the UID returned from the POST request.

```bash
curl -X 'PATCH' \
  'http://localhost:8000/api/v1/books/{book_uid}' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Designing Data-Intensive Applications - 2nd Edition",
  "page_count": 650
}'
```

3.Delete a Book (DELETE)

Deleting a record generates a "Delete" event and a "Tombstone" message in Kafka to ensure the record is also removed from the PostgreSQL sink.

Note: Replace {book_uid} with the UID returned from the POST request.

```bash
curl -X 'DELETE' \
  'http://localhost:8000/api/v1/books/{book_uid}' \
  -H 'accept: application/json'
```

#### Verify the CDC Result

1.Check PostgreSQL (The Sink):

After running any of the commands above, check your target database to confirm the synchronization:
```bash
# Connect to your Postgres instance
psql -d lib -U postgres
SELECT * FROM books;
```
2.Observe Avro Messages

Since the data is serialized in Avro, use the specific console consumer to read data.
```bash
bin/kafka-avro-console-consumer --bootstrap-server localhost:9092 \
  --property map.deep.nulls=true \
  --property schema.registry.url=http://localhost:8081 \
  --topic data.lib.users --from-beginning
```
