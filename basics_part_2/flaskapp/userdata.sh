#!/bin/bash
yum update -y
yum install -y python3 httpd mod_wsgi.x86_64 git
cd ~ && git clone https://github.com/aws-samples/virtual-immersion-week-labs.git
cd virtual-immersion-week-labs/lambda_ec2
cp flaskapp/vhost.conf /etc/httpd/conf.d/vhost.conf
cd flaskapp && rm vhost.conf
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
python3 -m pip install flask
deactivate
cd ..
cp -R flaskapp /var/www/html
mkdir /var/www/html/flaskapp/data
chmod 0777 /var/www/html/flaskapp/data
service httpd start
