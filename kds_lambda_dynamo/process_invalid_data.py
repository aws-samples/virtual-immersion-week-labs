import boto3
import datetime
import json
import os
import tempfile


S3_BUCKET = os.environ.get('S3_BUCKET') or None


s3 = boto3.client('s3')


def store_in_s3(data):
    cur_date = datetime.datetime.utcnow()
    s3_prefix = cur_date.strftime('%Y/%m/%d/')
    s3_key = s3_prefix + cur_date.strftime('%H%M%S-data.json')
    
    with tempfile.NamedTemporaryFile() as tmpfile:
        
        tmpfile.write(json.dumps(data).encode('UTF-8'))
        tmpfile.flush()
        
        with open(tmpfile.name, 'rb') as bfile:
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=bfile)


def lambda_handler(event, context):
    
    records = event['Records']
    data = [r for r in map(lambda x: x['body'], records)]
    store_in_s3(data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
