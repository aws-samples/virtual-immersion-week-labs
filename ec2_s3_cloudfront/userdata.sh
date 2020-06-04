#!/bin/bash
yum update -y
yum install -y python3 httpd mod_wsgi.x86_64 git
python3 -m pip install virtualenv boto3

# Copy data from S3
cd ~
mkdir flaskapp && cd flaskapp
python3 -c "import boto3; ci=boto3.client('cognito-identity',region_name='eu-west-1'); i=ci.get_id(IdentityPoolId='eu-west-1:68ced095-1051-4158-8818-ad47d5bf9ffd'); cd=ci.get_credentials_for_identity(IdentityId=i['IdentityId'])['Credentials']; s3=boto3.client('s3',aws_access_key_id=cd['AccessKeyId'],aws_secret_access_key=cd['SecretKey'],aws_session_token=cd['SessionToken'],region_name='eu-west-1'); s3.download_file('immersion-week-ec2-20200520', 'flaskapp.zip', 'flaskapp.zip');"
unzip flaskapp.zip
mv vhost.conf /etc/httpd/conf.d/vhost.conf
rm flaskapp.zip

# Create the virtual environment for the WSGI app and populate it.
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install flask requests
deactivate

# Copy the app to the HTTP server root, and restart the server.
cd ..
cp -R flaskapp /var/www/html
service httpd restart