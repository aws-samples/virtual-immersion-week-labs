import boto3
import csv
import json
import tempfile

from scapy.all import *


DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE') or 'PacketCaptures'
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def dump_table_to_s3(bucket, name, table):
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as ftmp:
        fieldnames=['src', 'dst', 'len', 'proto']
        writer = csv.DictWriter(ftmp, fieldnames=fieldnames)
    
        writer.writeheader()
        for row in table:
            writer.writerow(row)
    
        ftmp.flush()

        key = 'csv/%s.csv' % name
        with open(ftmp.name, 'rb') as bfile:
            s3.put_object(Bucket=bucket, Key=key, Body=bfile)
        

def dump_table_to_dynamo(s3_id, data):

    table = dynamodb.Table(DYNAMODB_TABLE)
    table.put_item(
        Item={
            's3Id': s3_id,
            'packetData': data
        })


def generate_table(packets):
    table = []
    
    for packet in packets:
        if IP in packet:
            row = {
                'src': packet[IP].src,
                'dst': packet[IP].dst,
                'len': packet[IP].len if hasattr(packet[IP], 'len') else -1,
                'proto': 'ip'
            }
            table.append(row)
            
        if Ether in packet:
            row = {
                'src': packet[Ether].src,
                'dst': packet[Ether].dst,
                'len': packet[Ether].len if hasattr(packet[Ether], 'len') else -1,
                'proto': 'ether'
            }
            table.append(row)

    return table


def lambda_handler(event, context):
    
    s3_event = event['Records'][0].get('s3')
    if s3 is None:
        response = {
            'statusCode': 400,
            'body': json.dumps({'errorMessage': 'No S3 event.'})
        }
    else:
        bucket = s3_event['bucket']['name']
        key = s3_event['object']['key']
        
        response = s3.get_object(
            Bucket=bucket,
            Key=s3_event['object']['key'])
            
        base_key = key.split('/')[-1].split('.')[0]

        ftmp = tempfile.NamedTemporaryFile(delete=True)
        ftmp.write(response['Body'].read())
        ftmp.flush()
        
        packets = rdpcap(ftmp.name)
        ftmp.close()
        
        table = generate_table(packets)
        dump_table_to_s3(bucket, base_key, table)
        dump_table_to_dynamo('%s/%s' % (bucket, key), table)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
