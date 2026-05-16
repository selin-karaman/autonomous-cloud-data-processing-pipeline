# ⚙️ Autonomous-Cloud-Data-Processing-Pipeline
Autonomous-Cloud-Data-Processing-Pipeline is an event-driven, serverless data processing engine that runs completely locally on LocalStack. It demonstrates a fully automated data journey—from raw ingestion to persistent storage—by orchestrating AWS microservices as a resilient, decoupled system.

## 🌟 Key Features
* **Autonomous Event-Driven Flow:** Any file dropped into the S3 bucket automatically triggers an end-to-end processing lifecycle `(S3 → Lambda → SQS → Lambda → DynamoDB)` without any manual intervention or cron jobs.
* **Asynchronous Decoupling:** Implements Amazon SQS between the validation and processing layers to eliminate system bottlenecks, absorb traffic spikes, and guarantee zero data loss.
* **Smart Data Transformation:** Automatically handles the notorious float/numeric type mismatches between Python's boto3 and DynamoDB using serverless Decimal type serialization in the background.
* **Docker Optimization:** Specifically engineered to bypass network layer constraints, container loopbacks (host.docker.internal), and modern AWS CLI protocol mismatches (x-amz-trailer) on macOS.

## 🛠️ Tech Stack
* **Language:** Python 3.9 / 3.13
* **AWS Interaction:** Boto3 & AWS CLI v2
* **Local Simulation:** LocalStack 3.0.0 (Community Edition)
* **Infrastructure Layer:** Docker & Docker Compose

## 🚀 Quick Start
### 1. Prerequisites
Ensure you have Docker and Python installed on your system.

### 2. Launch Local Cloud
Spin up the LocalStack container infrastructure in the background:

```
docker-compose up -d
```


### 3. Provision Infrastructure
Run the Boto3-based automation script to provision all necessary S3 buckets, SQS queues, DynamoDB tables, and IAM roles:

```
python3 infra/setup_aws.py
```

### 4. Deploy & Trigger Pipeline
Package your Lambda deployment zips, update their function codes on LocalStack, and use curl to drop the first test payload into the ingestion pipeline:

```
curl -X PUT -T test_data.json http://localhost:4566/raw-data-bucket/test_data.json
```


## 🔍 Discovery Logic & Topology
The core engine executes a two-stage serverless architectural pattern to validate and persist the incoming data stream safely:

* **Validator Logic:** Triggered instantly by an S3 ObjectCreated:Put event. The first Lambda validates the raw JSON schema. Valid payloads are safely pushed into the SQS queue for decoupling.

* **Processor Logic:** Automatically processes records from the SQS message source mapping. The second Lambda transforms the data payload, applies business logic, and persists the sanitized state into the DynamoDB ProcessedData sink.

# 📊 Pipeline Execution in Action
Below is the verification of the fully functional event-driven pipeline. Running a live DynamoDB scan shows the successful otonom state transformation, reflecting the processed boolean flag and calculated metrics mapped dynamically through the local cloud layers:

```
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name ProcessedData
```
