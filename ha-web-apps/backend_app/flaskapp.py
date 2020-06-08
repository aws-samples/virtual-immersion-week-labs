#!/usr/bin/python3
import requests

from flask import Flask, request

app = Flask(__name__)
METADATA_ENDPOINT = 'http://169.254.169.254/latest'


def get_availability_zone():
    r = requests.put(METADATA_ENDPOINT + '/api/token', headers={'X-aws-ec2-metadata-token-ttl-seconds': '21600'})
    r = requests.get(METADATA_ENDPOINT + '/meta-data/placement/availability-zone', headers={'X-aws-ec2-metadata-token': r.text})
    return r.text

def build_cors_response(content):
    response = app.make_response(content)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "Cache-Control")
    response.headers.add('Access-Control-Allow-Methods', "GET, HEAD, OPTIONS")
    return response

@app.route('/', methods=['GET', 'OPTIONS'])
def index():
    if request.method == 'OPTIONS':
        content = ""
    else:
        content = get_availability_zone()

    return build_cors_response(content)


if __name__ == '__main__':
    app.run()
    