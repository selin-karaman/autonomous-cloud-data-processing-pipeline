import json
import boto3
import os

ENDPOINT_URL = "http://host.docker.internal:4566"
sqs = boto3.client("sqs", endpoint_url=ENDPOINT_URL, region_name="us-east-1")
QUEUE_URL = f"{ENDPOINT_URL}/000000000000/validated-data-queue"

def handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)
        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(response['Body'].read().decode('utf-8'))
        
        if "id" in data and "amount" in data:
            sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(data)
            )
            return {"status": "validated"}
        else:
            return {"status": "invalid_data"}