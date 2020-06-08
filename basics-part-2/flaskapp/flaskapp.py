#!/usr/bin/python3
import datetime
import json
import os

UPDATED_FILENAME = '/var/www/html/flaskapp/data/updated.txt'
TOKEN_FILENAME = '/var/www/html/flaskapp/data/sns_token.txt'

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    html = '<html><head><title>Hello from Flask!</title></head>'
    html = '%s<body><h1>Hello from Flask!</h1>' % html

    if os.path.exists(UPDATED_FILENAME):
        with open(UPDATED_FILENAME, 'r') as f:
            timestamp = f.read()
    else:
        timestamp = 'Never updated'

    html = '%s<h2>%s</h2></body></html>' % (html, timestamp)
    return html

@app.route('/update', methods=['POST'])
def update():

    header_value = request.headers.get('x-amz-sns-message-type')
    if header_value is not None and header_value == 'SubscriptionConfirmation':
        with open(TOKEN_FILENAME, 'wt') as f:
            f.write('Token = %s' % json.loads(request.data)['Token'])
    else:
        with open(UPDATED_FILENAME, 'wt') as f:
            f.write('Updated on %s UTC' % str(datetime.datetime.utcnow()))
    return '', 204

@app.route('/get_token', methods=['GET'])
def get_token():
    if os.path.exists(TOKEN_FILENAME):
        with open(TOKEN_FILENAME, 'r') as f:
            token = f.read()
    else:
        token = 'Not on this server.'
    
    html = '<html><head><title>Token</title></head><body>SNS token: %s</body></html>' % token
    return html

if __name__ == '__main__':
    app.run()