#!/bin/bash

AWS_REGION=`aws configure get region`
ROLE_NAME="Cloud9-myLambdaRole"
S3_BUCKET_PREFIX="viw-lambda-ec2-lab"
LAB_DIRECTORY="basics-part-2"

# Delete all directories not related to this lab.
# (mindepth=1 excludes . and .., maxdepth=1 excludes subdirectories.)
find -mindepth 1 -maxdepth 1 -type d ! -iname $LAB_DIRECTORY -print0 | xargs -0 rm -Rf

ACCOUNTID=`aws sts get-caller-identity \
    | python -c "import json; import sys; print(json.load(sys.stdin)['Account'])"`
echo "Initializing account ID $ACCOUNTID"

echo "Creating role $ROLE_NAME"
ROLE_ARN=`aws iam create-role \
    --role-name "$ROLE_NAME" \
    --assume-role-policy-document file://lambda-role.json \
    | python -c "import json; import sys; print(json.load(sys.stdin)['Role']['Arn'])"`


echo "Role ARN: $ROLE_ARN"
echo "Attaching policies"
aws iam attach-role-policy --role-name $ROLE_NAME \
    --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"
aws iam attach-role-policy --role-name $ROLE_NAME \
    --policy-arn "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
aws iam attach-role-policy --role-name $ROLE_NAME \
    --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
aws iam attach-role-policy --role-name $ROLE_NAME \
    --policy-arn "arn:aws:iam::aws:policy/AmazonSNSFullAccess"


BUCKET_NAME="${S3_BUCKET_PREFIX}-$ACCOUNTID"
echo "Creating S3 bucket $BUCKET_NAME"
aws s3api create-bucket --bucket $BUCKET_NAME --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_REGION

# Build the Scapy layer to be used during the Lambda function exercise.

rm -Rf /tmp/scapy_layer
mkdir /tmp/scapy_layer
cd /tmp/scapy_layer
python3 -m pip install scapy -t .
mkdir python && cd python && mv ../scapy ./ && cd ..
zip -r scapy_layer.zip python > /dev/null

aws s3 cp /tmp/scapy_layer/scapy_layer.zip s3://$BUCKET_NAME/scapy_layer.zip
