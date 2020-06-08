import boto3
import json
import os


DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE') or None


dynamodb = boto3.resource('dynamodb')


def store_in_dynamo(data):
    table = dynamodb.Table(DYNAMODB_TABLE)
    
    for entry in data:
        entry['DataId'] = str(entry['timestamp'])
        table.put_item(Item=entry)


def lambda_handler(event, context):
    
    records = event['Records']
    data = [json.loads(r) for r in map(lambda x: x['body'], records)]
    store_in_dynamo(data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
