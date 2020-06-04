# Virtual Immersion Week Lab - Serverless with AWS Lambda, Amazon Kinesis, Amazon SQS, and Amazon S3

## Objective

The objective of this lab is to give you basic hands-on experience for building serverless applications using AWS Lambda to run functions without servers, Amazon Kinesis to ingest data from a variety of sources, Amazon SQS to decouple different parts of an application, and Amazon S3 for data storage.

## Architecture

<p align="center">
    <img alt="architecture_diagram" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/architecture_diagram.png" width="85%">
</p>

## Steps

So that you can concentrate on learning about the core services used in this laboratory, a few resources have been configured for you. These include the roles you will be using for your Lambda functions

Let's start by creating the resources that Lambda functions will be built around: the Kinesis data stream, the SQS queues and the S3 buckets.

### Create a Cloud9 environment

Click on the Services menu at the top left corner of the screen, and enter **Cloud9** into the search bar, then click on the *Cloud9* menu item.

<p align="center">
    <img alt="kinesis_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_1.PNG" width="25%">
</p>

Click on the *Create environment* button to start creating a new environment.

<p align="center">
    <img alt="kinesis_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_2.PNG" width="55%">
</p>

Enter **MyCloud9Environment** in the *Name* field, and click on the *Next step* button to continue.

<p align="center">
    <img alt="kinesis_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_3.PNG" width="85%">
</p>

Leave the rest as it is, and click on the *Next step* button to continue.

<p align="center">
    <img alt="kinesis_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_4.PNG" width="85%">
</p>

Review the parameters and click on the *Create environment* button.

<p align="center">
    <img alt="kinesis_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_5.PNG" width="85%">
</p>

After a brief setup process, you will be taken to your newly created Cloud9 environment. 

<p align="center">
    <img alt="kinesis_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_6.PNG" width="85%">
</p>

In the terminal tab at the bottom of the page, enter

```
wget https://ee-assets-prod-us-east-1.s3.amazonaws.com/modules/fd930fe5e13041569faef727a4e84051/v1/kds_lambda_dynamo.tar.gz
```

<p align="center">
    <img alt="kinesis_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_7.PNG" width="85%">
</p>

And then decompress the file by running
```
tar xzf kds_lambda_dynamo.tar.gz
```

<p align="center">
    <img alt="kinesis_8" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_8.PNG" width="85%">
</p>

You should see the following files appear at the top left corner, in the project tree.

<p align="center">
    <img alt="kinesis_9" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/cloud9_9.PNG" width="35%">
</p>

Now your environment has been prepared with all the necessary data. As next steps, you will create the resources used by the Lambda functions.

**Note**: *Keep your Cloud9 window open, as you will need to retrieve code from the files you just unpacked as you advance through the steps.*

### Creating the Kinesis data stream

Click on the Services menu at the top left corner of the screen, and enter **Kinesis** into the search bar, then click on the *Kinesis* menu item.

<p align="center">
    <img alt="kinesis_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/kinesis_0.PNG" width="35%">
</p>

Click on the *Create data stream* button on the right side of the screen.

<p align="center">
    <img alt="kinesis_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/kinesis_1.PNG" width="85%">
</p>

Name the data stream **ClientDataStream**, then enter **1** in the *Number of open shards* field. Then, click on the *Create data stream* button.

<p align="center">
    <img alt="kinesis_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/kinesis_2.PNG" width="85%">
</p>

Your Kinesis data stream is ready to ingest data.

### Create the SQS queues

Click on the Services menu at the top left corner of the screen, and enter **SQS** into the search bar, then click on the SQS menu item.

<p align="center">
    <img alt="sqs_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/sqs_0.PNG" width="35%">
</p>

Click on the *Get Started Now* button.

<p align="center">
    <img alt="sqs_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/sqs_1.PNG" width="85%">
</p>

In *Queue Name*, enter the name of the first queue, **AveragedDataQueue**. Make sure you use a *Standard Queue*, then click on the *Quick-Create Queue* button.

<p align="center">
    <img alt="sqs_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/sqs_2.PNG" width="85%">
</p>

Your first queue, **AveragedDataQueue**, has just been created. Continue with the second queue, **InvalidDataQueue**.

Click on the *Create New Queue* button.

<p align="center">
    <img alt="sqs_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/sqs_3.PNG" width="85%">
</p>

In *Queue Name*, enter the name of the second queue, **InvalidDataQueue**. Make sure you use a *Standard Queue* as in the first case, then click on the *Quick-Create Queue* button.

<p align="center">
    <img alt="sqs_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/sqs_4.PNG" width="85%">
</p>

SQS queues are now ready to be used, as well.

### Create the S3 buckets

Information ingested through Kinesis and processed by the **ProcessStreamingData** Lambda function will be stored for future use in two different buckets. Data considered *invalid* will be sent to the **invalid-data-012345678901** bucket, whereas valid data will be stored in the **historical-data-012345678901** bucket for future use.

Please remember that the **012345678901** number at the end of both names is the AWS Account Number of the account you are using for this lab.

Click once again on the Services menu at the top left corner of your screen, type in **S3** in the search bar, and click on the S3 menu item.

<p align="center">
    <img alt="s3_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/s3_0.PNG" width="35%">
</p>

**Note**: *Make sure you use the new console. If not, some of the screens shown below may not look like your console does.*

<p align="center">
    <img alt="s3_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/s3_0a.PNG" width="85%">
</p>

Click on the *Create bucket* button.

<p align="center">
    <img alt="s3_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/s3_1.PNG" width="85%">
</p>

Enter the name of the bucket in the *Bucket name* field. This should start with **historical-data-** followed by your AWS Account Number. As the *Region* where the bucket will live, select **eu-west-1**.

Click on the *Create bucket* to create the first bucket.

<p align="center">
    <img alt="s3_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/s3_2.PNG" width="85%">
</p>

Now, once again, click on the *Create bucket* button. This time, you will name the bucket **invalid-data-** followed by your AWS Account Number. Select the same region as before, **eu-west-1**, and click on the *Create bucket* button to continue.

<p align="center">
    <img alt="s3_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/s3_3.PNG" width="85%">
</p>

### Create the DynamoDB table

The **ProcessStreamingData** function computes point-in-time averages that could be queried in real time by a dashboard. Thus, this data will be stored in a DynamoDB table, from which it can be swiftly retrieved.

To create this table, named **PointInTimeAverages**, first go to the DynamoDB console by clicking on the Services menu at the top left corner of the screen, type in **Dynamo** in the search box, and click on the **DynamoDB** menu item.

<p align="center">
    <img alt="dynamodb_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/dynamodb_0.PNG" width="35%">
</p>

Then, click on the **Create table** button in the middle of the screen to start creating the table.

<p align="center">
    <img alt="dynamodb_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/dynamodb_1.PNG" width="85%">
</p>

Enter **PointInTimeAverages** in the *Table name* field, and **DataId** in the *Primary key* field. This table will use the default settings, so click on the *Create* button to continue.

<p align="center">
    <img alt="dynamodb_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/dynamodb_2.PNG" width="85%">
</p>

### Create the ProcessStreamingData Lambda function.

Click on the Services menu at the top left corner of the screen, type in **Lambda** in the search bar, and click on the *Lambda* menu item.

<p align="center">
    <img alt="lambda_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_0.PNG" width="35%">
</p>

Once in the Lambda console, click on the *Create Function* button.

<p align="center">
    <img alt="lambda_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_1.PNG" width="85%">
</p>

In the *Function name* field, enter your function's name (**ProcessStreamingData**), then choose **Python 3.8** as its runtime.

Click on the *Choose or create an execution role* to unfold the section, and choose *Use an existing role*. Then, from the *Existing role* dropdown, choose the **ImmersionWeekProcessStreamingData** role.

Click on the *Create function* button at the bottom right corner of the screen to continue.

<p align="center">
    <img alt="lambda_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_2.PNG" width="85%">
</p>

Click on the *Designer* section to unfold the contents, then click on the *Add Trigger* button.

<p align="center">
    <img alt="lambda_2a" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_2a.PNG" width="85%">
</p>

From the service dropdown, choose *Kinesis*. Then, choose the **ClientDataStream** stream from the *Kinesis stream* dropdown. Set the *Batch size* to **100** and the *Batch window* to **60** seconds.

Then, click on the *Add* button to add the trigger.

<p align="center">
    <img alt="lambda_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_3.PNG" width="85%">
</p>

Now click on the *ProcessStreamingData* block in the *Designer* section to go back to the function code.

<p align="center">
    <img alt="lambda_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_4.PNG" width="85%">
</p>

Once the trigger has been created, copy the code from the **process_streaming_data.py** file that you have on your Cloud9 environment, and paste it into the tab named *lambda_function.py* in the *Function code* section. Then, click on the *Save* button at the top right corner of the screen.

<p align="center">
    <img alt="lambda_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_5.PNG" width="85%">
</p>

Configure the environment variables by scrolling down to the *Environment variables* section, and clicking on the *Edit* button on the right side of it.

<p align="center">
    <img alt="lambda_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_6.PNG" width="85%">
</p>

Here, create the following three variables and assign them the below listed values:

|Variable name|Value|
|---|---|
|AVERAGED_QUEUE_URL|https://sqs.eu-west-1.amazonaws.com/012345678901/AveragedDataQueue|
|INVALID_QUEUE_URL|https://sqs.eu-west-1.amazonaws.com/012345678901/InvalidDataQueue|
|S3_BUCKET|historical-data-012345678901|

where **012345678901** is your AWS Account number. Then, click on the *Save* button.

<p align="center">
    <img alt="lambda_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_7.PNG" width="85%">
</p>

### Create the ProcessInvalidData Lambda function.

Back on the Lambda console, click on the *Create function* button to create the next function, **ProcessInvalidData**, which will handle all data that is flagged as invalid.

<p align="center">
    <img alt="lambda_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_1.PNG" width="85%">
</p>

Enter the name of the function, **ProcessInvalidData** in the *Function name* field, then choose **Python 3.8** from the *Runtime* dropdown. Click on the *Choose or create an execution role* to unfold the section, then choose *Use an existing role* and from the *Existing role* dropdown, choose **ImmersionWeekProcessInvalidDataRole**.

Click on the *Create function* button at the bottom right corner of the screen to create the function.

<p align="center">
    <img alt="lambda_invalid_data_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_invalid_data_1.PNG" width="85%">
</p>

Click on the *Add trigger* button to add a trigger that fires this Lambda function every time there are messages in the **InvalidDataQueue** SQS queue.

<p align="center">
    <img alt="lambda_invalid_data_1b" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_invalid_data_1b.PNG" width="85%">
</p>

From the service dropdown, choose the *SQS* menu item. Then, click on the *SQS queue* field, and choose the **InvalidDataQueue** queue, and click on the *Add* button at the bottom right corner of the screen.

<p align="center">
    <img alt="lambda_invalid_data_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_invalid_data_2.PNG" width="85%">
</p>

Once the trigger has been created, click on the *ProcessInvalidData* block in the *Designer* section.

<p align="center">
    <img alt="lambda_invalid_data_2a" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_invalid_data_2a.PNG" width="85%">
</p>

Copy the code from the **process_invalid_data.py** file that you have on your Cloud9 environment, and paste it into the tab named *lambda_function.py* in the *Function code* section. Then, click on the *Save* button at the top right corner of the screen.

<p align="center">
    <img alt="lambda_invalid_data_2b" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_invalid_data_2b.PNG" width="85%">
</p>

Configure the environment variables by scrolling down to the *Environment variables* section, and clicking on the *Edit* button on the right side of it.

<p align="center">
    <img alt="lambda_invalid_data_2c" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_invalid_data_2c.PNG" width="85%">
</p>

Here, only a single environment variable needs to be configured. Use **S3_BUCKET** as its name, and set its value to **invalid-data-012345678901**, where **012345678901** is your AWS Account Number.

<p align="center">
    <img alt="lambda_invalid_data_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_invalid_data_3.PNG" width="85%">
</p>

### Create the StoreAverages Lambda function

Once again on the Lambda console, click on the *Create function* button to create the next function, **StoreAverages**, which will handle all the averages submitted by the **ProcessStreamingData** function to the **AveragedDataQueue** SQS queue.

<p align="center">
    <img alt="lambda_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_1.PNG" width="85%">
</p>

Enter the name of the function, **StoreAverages** in the *Function name* field, then choose **Python 3.8** from the *Runtime* dropdown. Click on the *Choose or create an execution role* to unfold the section, then choose *Use an existing role* and from the *Existing role* dropdown, choose **ImmersionWeekStoreAveragesRole**.

Click on the *Create function* button at the bottom right corner of the screen to create the function.

<p align="center">
    <img alt="lambda_averages_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_averages_1.PNG" width="85%">
</p>

Click on the *Add trigger* button to add a trigger that fires this Lambda function every time there are messages in the **AveragedDataQueue** SQS queue.

<p align="center">
    <img alt="lambda_averages_1a" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_averages_1a.PNG" width="85%">
</p>

From the service dropdown, choose the *SQS* menu item. Then, click on the *SQS queue* field, and choose the **AveragedDataQueue** queue, set the batch size to **1**, and click on the *Add* button at the bottom right corner of the screen.

<p align="center">
    <img alt="lambda_averages_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_averages_2.PNG" width="85%">
</p>

Once the trigger has been created, click on the *StoreAverages* block in the *Designer* section.

<p align="center">
    <img alt="lambda_averages_2a" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_averages_2a.PNG" width="85%">
</p>

Copy the code from the **store_averages.py** file that you have on your Cloud9 environment, and paste it into the tab named *lambda_function.py* in the *Function code* section. Then, click on the *Save* button at the top right corner of the screen.

<p align="center">
    <img alt="lambda_averages_2b" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_averages_2b.PNG" width="85%">
</p>

Configure the environment variables by scrolling down to the *Environment variables* section, and clicking on the *Edit* button on the right side of it.

<p align="center">
    <img alt="lambda_averages_2c" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_averages_2c.PNG" width="85%">
</p>

Again, only a single environment variable needs to be configured. Use **DYNAMODB_TABLE** as its name, and set its value to **PointInTimeAverages**.

<p align="center">
    <img alt="lambda_averages_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/lambda_averages_3.PNG" width="85%">
</p>

## Feeding data to the Kinesis stream

Return to your Cloud9 environment, and double-click on the **data_generator.py** file at the top left corner of the project tree to open the file. Then, click on the *Run* button to execute it.

<p align="center">
    <img alt="data_generator_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/data_generator_1.PNG" width="85%">
</p>

Once the generator runs, you should see the following output:

<p align="center">
    <img alt="data_generator_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/data_generator_2.PNG" width="85%">
</p>

Run the script a few more times to generate abundant data. In a matter of a few seconds, you should start seeing your S3 buckets populating:

<p align="center">
    <img alt="s3_historical_data" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/s3_historical_data.PNG" width="85%">
</p>

<p align="center">
    <img alt="s3_invalid_data" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/s3_invalid_data.PNG" width="85%">
</p>

As well as your DynamoDB table.

<p align="center">
    <img alt="dynamodb_results" src="https://github.com/aws-samples/virtual-immersion-week-labs/kds_lambda_dynamo/raw/master/img/dynamodb_results.PNG" width="85%">
</p>
