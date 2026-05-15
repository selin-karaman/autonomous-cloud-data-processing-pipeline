import boto3

AWS_REGION = "us-east-1"
ENDPOINT_URL = "http://localhost:4566"

s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL, region_name=AWS_REGION)
sqs = boto3.client("sqs", endpoint_url=ENDPOINT_URL, region_name=AWS_REGION)
dynamodb = boto3.client("dynamodb", endpoint_url=ENDPOINT_URL, region_name=AWS_REGION)

def setup_infrastructure():
    s3.create_bucket(Bucket="raw-data-bucket")
    
    sqs.create_queue(QueueName="validated-data-queue")
    
    try:
        dynamodb.create_table(
            TableName="ProcessedData",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )
    except dynamodb.exceptions.ResourceInUseException:
        pass

if __name__ == "__main__":
    setup_infrastructure()