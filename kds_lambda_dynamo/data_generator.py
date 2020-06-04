#!/env/bin/python
import boto3
import datetime
import ipaddress
import json
import random
import sys
import time


# Define a CIDR range for the theoretical network.
CIDR_RANGE = '10.0.7.0/24'

# Get all available IPs for the CIDR range.
AVAILABLE_IPS = [str(ip) for ip in ipaddress.IPv4Network(CIDR_RANGE)]

# Number of records to send per request.
RECORDS_PER_REQUEST = 25

# Percentage, expressed as a coefficient, of succesful requests.
K_SUCCESSFUL_REQUESTS = 0.80

# The absolute number of milliseconds that timestamps for fake requests can deviate
# from the current date.
JITTER_MILLISECONDS = 100

# Minimum latency to assign to fake requests.
MIN_LATENCY_MS = 10

# Maximum latency to assign to fake requests.
MAX_LATENCY_MS = 300


def get_epoch(dt: datetime.datetime) -> int:
    return (dt-datetime.datetime(year=1970, month=1, day=1)).total_seconds()


def generate_data():
    
    records = []
    
    n_record = RECORDS_PER_REQUEST
    while n_record > 0:
        idx = random.randrange(0, len(CIDR_RANGE))
        
        dms = random.randrange(-JITTER_MILLISECONDS, JITTER_MILLISECONDS+1)
        ts = datetime.datetime.utcnow() + datetime.timedelta(milliseconds=dms)
        
        records.append({
            'ip': AVAILABLE_IPS[idx],
            'timestamp': get_epoch(ts),
            'latency': random.randrange(MIN_LATENCY_MS, MAX_LATENCY_MS),
            'valid': True if random.random() <= K_SUCCESSFUL_REQUESTS else False,
        })
        n_record = n_record - 1
    
    
    return records


def calculate_mean_latency_per_ip(data):
    hashtable = {}
    results = {}
    
    for entry in data:
        print (entry['ip'], entry['latency'])
        hashtable.setdefault(entry['ip'], []).append(entry['latency'])
    
    results = {k:v for (k,v) in map(lambda k: (k, sum(hashtable[k])/len(hashtable[k])), hashtable.keys())}

    return results


def get_kinesis_record(record):
    result = {
        'Data': json.dumps(record).encode('UTF-8'),
        
        # We're using only one shard, so there's no effect if this is hardcoded.
        'PartitionKey': 'partition-key'
    }
    return result

 
kinesis = boto3.client('kinesis')
data = generate_data()

for i in range(0, 10):
    records = [r for r in map(lambda x: get_kinesis_record(x), data)]
    
    response = kinesis.put_records(
        StreamName='ClientDataStream',
        Records=records
    )
    time.sleep(0.25)
    print (f"{len(records)} records sent, failed {response['FailedRecordCount']}")
