#!/bin/bash

AWS_REGION=`aws configure get region`
ROLE_NAME="Cloud9-myRedshiftRole"
S3_BUCKET_PREFIX="redshift-demo"
S3_TICKIT_ORIGIN="s3://awssampledbuswest2/tickit/"
TICKIT_FILES=("allevents_pipe.txt" "allusers_pipe.txt" "category_pipe.txt" \
    "date2008_pipe.txt" "listings_pipe.txt" "sales_tab.txt" "venue_pipe.txt")

ACCOUNTID=`aws sts get-caller-identity \
    | python -c "import json; import sys; print(json.load(sys.stdin)['Account'])"`

echo "Initializing environment for account $ACCOUNTID"

echo "Creating role $ROLE_NAME"
ROLE_ARN=`aws iam create-role \
    --role-name "$ROLE_NAME" \
    --assume-role-policy-document file://redshift-role.json \
    | python -c "import json; import sys; print(json.load(sys.stdin)['Role']['Arn'])"`

echo "Role ARN: $ROLE_ARN"
echo "Attaching policies"
aws iam attach-role-policy --role-name $ROLE_NAME \
    --policy-arn "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
aws iam attach-role-policy --role-name $ROLE_NAME \
    --policy-arn "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"

BUCKET_NAME="${S3_BUCKET_PREFIX}-$ACCOUNTID"
echo "Creating S3 bucket $BUCKET_NAME"
aws s3api create-bucket --bucket $BUCKET_NAME --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=eu-west-1

echo "Populating bucket."
for tickit_file in ${TICKIT_FILES[@]}; do
    SOURCE_FILE="${S3_TICKIT_ORIGIN}${tickit_file}"
    TARGET_FILE="s3://$BUCKET_NAME/tickit/${tickit_file}"
    echo "Copying $SOURCE_FILE to $TARGET_FILE"
    aws s3 cp $SOURCE_FILE $TARGET_FILE
done

aws s3 cp s3://awssampledbuswest2/tickit/spectrum/sales/ "s3://$BUCKET_NAME/tickit/spectrum/sales/" \
    --recursive

echo "Account setup successfully."
