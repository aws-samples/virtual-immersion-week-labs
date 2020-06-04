import base64
import boto3
import datetime
import json
import os
import tempfile


AVERAGED_QUEUE_URL = os.environ.get('AVERAGED_QUEUE_URL') or None
INVALID_QUEUE_URL = os.environ.get('INVALID_QUEUE_URL') or None
S3_BUCKET = os.environ.get('S3_BUCKET') or None


sqs = boto3.client('sqs')
s3 = boto3.client('s3')

def get_epoch(dt: datetime.datetime) -> int:
    return (dt-datetime.datetime(year=1970, month=1, day=1)).total_seconds()


def post_invalid_data(data):
    sqs.send_message(
        QueueUrl=INVALID_QUEUE_URL,
        MessageBody=json.dumps(data))


def calculate_mean_latency_per_ip(data):
    hashtable = {}
    results = {}
    
    for entry in data:
        hashtable.setdefault(entry['ip'], []).append(entry['latency'])
    
    results = {k:v for (k,v) in map(lambda k: (k, int(sum(hashtable[k])/len(hashtable[k]))), hashtable.keys())}
    return results


def process_valid_data(data):
    
    processed_data = calculate_mean_latency_per_ip(data)
    sqs.send_message(
        QueueUrl=AVERAGED_QUEUE_URL,
        MessageBody=json.dumps({
            'timestamp': int(get_epoch(datetime.datetime.utcnow())),
            'processedData': processed_data
        }))

        
def store_historical_data(data):
    cur_date = datetime.datetime.utcnow()
    s3_prefix = cur_date.strftime('%Y/%m/%d')
    s3_key = "%s/%s" % (s3_prefix, cur_date.strftime('%H%m%s-data.json'))
    print (s3_key)

    with tempfile.NamedTemporaryFile() as tmpfile:
        tmpfile.write(json.dumps(data).encode('UTF-8'))

        with open(tmpfile.name, 'rb') as bfile:
            s3.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=bfile)


def lambda_handler(event, context):

    valid_data = []
    
    records = event['Records']
    for r in records:
        data = json.loads(base64.b64decode(r['kinesis']['data']))
        if data['valid'] == True:
            valid_data.append(data)
        else:
            post_invalid_data(data)
        
    process_valid_data(valid_data)
    store_historical_data(valid_data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
