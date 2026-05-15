import json
import boto3
from decimal import Decimal 

ENDPOINT_URL = "http://host.docker.internal:4566"
dynamodb = boto3.resource("dynamodb", endpoint_url=ENDPOINT_URL, region_name="us-east-1")
table = dynamodb.Table("ProcessedData")

def handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])

        body['processed'] = True
       
        calculated_amount = float(body['amount']) * 1.2
        body['amount'] = Decimal(str(calculated_amount))
        
        table.put_item(Item=body)
        
    return {"status": "processed_and_saved"}