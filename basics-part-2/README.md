# Basics of Networking, Compute and Event-Driven Architectures (Part 2)

## Objective

The objective of this lab is to help you understand how to model and implement event-driven architectures on AWS. Additionally, it should help you understand the basics of:

 * Load balancing in AWS using Amazon ELB and Amazon EC2 instances.
 * Creating and querying an Amazon DynamoDB table.
 * Reusing code in AWS Lambda functions by placing it in a Lambda layer.

## Initialize your environment

### 1. Create a AWS Cloud9 environment.

From the services menu, choose AWS Cloud9.

![cloud9_0](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cloud9_create_0.png "")

Click on the _Create environment_ button on the right side of the page.

![cloud9_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cloud9_create_1.png "")

Now, enter the name of your AWS Cloud9 environment: **MyCloud9Environment** in the _Name_ field, and click on _Next step_.

![cloud9_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cloud9_create_2.png "")

Leave the choices as default, since we want:
 * A new instance for the environment running on EC2.
 * The instance to be a **t2.micro** type of instance.
 * To install Amazon Linux on the t2.micro instance.

Then, click on _Next step_.

![cloud9_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cloud9_create_3.png "")

Review the information and click on _Create environment_.

![cloud9_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cloud9_create_4.png "")

### 2. Within the AWS Cloud9 instance that you just created obtain a copy of this repository.

Make sure you are in your environment directory.
```sh
cd ~/environment
```

Then run the following git command to clone the repository:
```sh
git clone https://github.com/aws-samples/virtual-immersion-week-labs.git && cd virtual-immersion-week-labs/basics-part-2
```

### 3. Run the initialization script to automatically create an S3 bucket and populate it.
```
bash initialize.sh
```

## Create DynamoDB table.

From the _Services_ menu, choose _DynamoDB_ and click it.

![dynamo_0](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/dynamo_create_0.png "")

At the main DynamoDB screen, click on the _Create table_ button at the center.

![dynamo_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/dynamo_create_1.png "")

Now you need to give the table a name and configure its settings.
 * Enter **PacketCaptures** into the _Table name_ field.
 * For the partition key, enter **captureId** into the _Primary key_ field and leave _String_ as the type of the field.

We will use the default settings for this demo, so go ahead and click on the _Create_ button at the bottom right corner of the screen.

![dynamo_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/dynamo_create_2.png "")

You will be taken to the main table screen, where you will be presented with an overview of the table and a series of tabs to access the different features in a table. For now, we are just interested in making sure the table is empty.

Click on the _Items_ tab at the center top portion of the screen.

![dynamo_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/dynamo_create_3.png "")

You will now be presented with a screen like the one below. Note that the number of total items is zero, and that there are no items whatsoever listed below.

![dynamo_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/dynamo_create_4.png "")

## Create SNS topic

On the _Services menu_, type in **SNS** in the search bar, and click on the _Simple Notification Service_ service link.

![sns_0](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_topic_0.png "")

Enter the **PacketCaptureProcessorTopic** in the _Topic name_ field, and click on the _Next step_ button below.

![sns_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_topic_1.png "")

We will not be filling in any optional data, so you can safely click on the _Create topic_ button at the lower right corner of the screen.

![sns_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_topic_2.png "")

You have created an SNS topic, which we will be using later on in this tutorial. Let's move on to creating our Lambda function.

## Create Lambda layer

On the _Services menu_, type in **Lambda** in the search bar, and click on the _Lambda_ service link.

![lambda_0](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_0.png "")

On the sidebar on your left, click on the _Layers_ menu item.

![lambda_layers_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_layers_1.png "")

Then, click on the _Create layer_ at the top right corner of the screen.

![lambda_layers_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_layers_2.png "")

You will be taken to the Create layer screen. Since we're creating a layer for Scapy to be available to a number of Lambda functions, we will name it accordingly:

 * Type **ScapyLayer** into the _Name_ field.
 * Select _Upload a file from Amazon S3_.
 * In the _Amazon S3 link URL_ text field, enter the URL to the file within the bucket that was created for you. It is **s3://viw-lambda-ec2-lab-012345678901/scapy_layer.zip**, where 012345678901 is the number of the AWS account that you are currently logged using.
 * From the _Compatible runtimes - optional_ dropdown, choose **Python 3.8**.

Once you are done, click on the _Create_ button at the bottom right corner.

![lambda_layers_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_layers_3.png "")

## Create Lambda function

Now we will move on to creating the actual Lambda function that will process the cap/pcap files uploaded into the S3 bucket.

From the sidebar on your left, click on _Functions_.

![lambda_functions_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_1.png "")

Then, click on the _Create function_ button at the top right corner.

![lambda_functions_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_2.png "")

Leaving the _Author from scratch_ option that is selected by default, enter the lambda function settings:

 * Into the _Function name_ text field, enter **PacketCaptureProcessorFunction**. This will be the name of our Lambda function.
 * From the _Runtime_ dropdown, choose **Python 3.8**.
 * Click on _Choose or create an execution role_ to reveal more options.
 * From the _Execution role_ radio button set, choose _Use an existing role_.
 * From the _Existing role_ dropdown, choose **Cloud9-myLambdaRole**.
 
Now you are ready to create the function. Click on the _Create function_ button at the bottom right corner of the screen.

![lambda_functions_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_3.png "")

Now, click on the _Layers_ block in the _Designer_ section.

![lambda_functions_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_4.png "")

Click on _Add a layer_ button in the _Layers_ section below.

![lambda_functions_5](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_5.png "")

From the _Name_ dropdown, choose **ScapyLayer**. And from the _Version_ dropdown, choose **1**.

Click on the _Add_ button to continue.

![lambda_functions_6](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_6.png "")

### Add S3 trigger

Now we will be adding an S3 trigger, so that every time a **.cap** file is uploaded to our bucket, the lambda function is invoked.

Click on the _Add trigger_ button in the _Designer_ section.

![lambda_functions_7](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_7.png "")

From the _Trigger configuration_ dropdown, select _S3_. Then, from the _Bucket_ dropdown, select your bucket. _Remember your bucket starts with_ **viw-lambda-ec2-lab-** _followed by your account ID_.

Leave **All object create events** in the _Event type_ dropdown, and enter **.cap** into the _Suffix_ text field.

Then, click on the _Add_ button at the bottom right corner of the screen.

![lambda_functions_8a](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_8a.png "")

### Add code to Lambda

Go back to your AWS Cloud9 editor, open the **lambda.py** file and copy the contents to the clipboard.

![lambda_functions_8b](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_8b.png "")

Now, go back to your Lambda tab. Click on the _PacketCaptureProcessorFunction_ block in the _Designer_ section, and paste the code into the _lambda_function.py_ tab in the _Function code_ section.

Then, click on the _Save_ button at the top right corner of the screen.

![lambda_functions_9](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_functions_9.png "")

### Add event to SNS

We will now add the SNS topic we created as a destination for an event whenever the Lambda function finishes with a success condition.

Click on the _Add destination_ button in the _Designer_ section.

![lambda_sns_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_sns_1.png "")

Now set up the destination as follows.

 * From _Source_ choose _Asynchronous invocation_.
 * Then, from _Condition_, choose _On success_.
 * From the _Destination type_ dropdown, choose _SNS topic_.
 * And from the _Destination_ dropdown, choose the **PacketCaptureProcessorTopic** that you previously created.
 
Then, click on the _Save_ button at the bottom right corner.

![lambda_sns_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/lambda_sns_2.png "")

## Create EC2 instances

Once again, on the _Services_ menu, enter **EC2** in the search bar, and click on the EC2 service link.

![ec2_0](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_0.png "")

Click on the _Instances_ menu item on the sidebar on the left.

![ec2_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_1.png "")

Click on the _Launch Instance_ button at the top center portion of the screen.

![ec2_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_2.png "")

Select the **Amazon Linux 2 AMI** from the list, by clicking on the _Select_ button next to it.

![ec2_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_3.png "")

Check the **t2.micro** instance to select it, then click on _Next: Configure Instance Details_ button at the bottom right corner of the screen.

![ec2_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_4.png "")

Now we'll configure some of the instance details.

 * Select the VPC you created in the previous module, **YourVPCName**, from the _Network_ dropdown.
 * Select one of the private subnets you created from the _Subnet_ dropdown.
 * Go back to your AWS Cloud9 environment tab, and copy the contents of the **userdata.sh** file in the **flaskapp** directory. Then, paste the contents of this file into the _User data_ text area at the bottom of the screen.
 * Click on _Next: Add Storage_
 
![ec2_5](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_5.png "")

This is how your **userdata.sh** contents should look like:

![ec2_6](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_6.png "")

Leave the storage settings as they are.

![ec2_6b](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_6b.png "")

Click on _Next: Add Tags_

Click on _Next: Configure Security Group_

Click on _Select an existing security group_, check the **WebServerSG** from the list, and move on to the next screen by clicking the _Review and launch_ button at the bottom right corner of the screen.

![ec2_7](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_7.png "")

Click on the _Launch_ button at the bottom right corner of the screen.

This will open a dialog that prompts you to create or choose an existing key pair.
 * Choose _Create a new key pair_, and enter **webserver** into the _Key pair name_ text field.
 * Click on the _Download Key Pair_ button to download the private key. You will use this private key in a moment.
 * Click on _Launch Instances_.
 
![ec2_8](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/ec2_8.png "")
 
Repeat the above procedure for a second EC2 instance that sits in the second private subnet.
**Note**: The second time you go through the procedure, instead of creating a new key pair in the last step, just select **webserver** from the key pair list, and check the _I acknowledge..._ box.

## Configure ELB.

We now need to configure the target group you created in the Networking part of this lab, so that the load balancer can redirect traffic to the instance we just created.

Find the _Target Groups_ menu item in the sidebar on your left, and click on it.

![elb_tg_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/elb_tg_1.png "")

If not already selected, select the _myTargetGroup_ target group by checking the box next to it. If you have multiple target groups, make sure this is the only one selected.

![elb_tg_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/elb_tg_2.png "")

Click on the _Targets_ tab in the section at the bottom of the screen.

![elb_tg_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/elb_tg_3.png "")

Click on the _Edit_ button to edit the targets to which the ELB will route the traffic.

![elb_tg_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/elb_tg_4.png "")

A dialog will appear. Check both instances you just created, and click the _Add to registered_ button on top of them.

![elb_tg_5](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/elb_tg_5.png "")

This is how it should like after you added them to the target group. You can now safely click on the _Save_ button.
![elb_tg_6](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/elb_tg_6.png "")

## Check website

Let's check whether the EC2 instances are running and serving the application that has been installed on them. Still in the EC2 console, look for and click on the _Load Balancers_ menu item on the sidebar to the left.

![cw_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cw_1.png "")

Make sure that the ELB you created in the previous section of this lab is selected. If there is more than one load balancer, make sure only **MyLoadBalancer** is checked. You also have to make sure it is active before you continue.

![cw_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cw_2.png "")

Find the _DNS name_ in the _Description_ tab in the section below, and copy the DNS name of the LB.

![cw_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cw_3.png "")

Enter the URL into a new browser tab. This is how it shoud look like:

![cw_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/cw_4.png "")

## Create SNS subscription

On the _Services menu_, type in **SNS** in the search bar, and click on the _Simple Notification Service_ service link.

![sns_0](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_topic_0.png "")

Click the _Subscriptions_ item on the sidebar to your left.

![sns_sub_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_1.png "")

Now click on the _Create subscription_ button.

![sns_sub_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_2.png "")

Now we need to fill out the details of the subscription we want to create:

 * Click the _Topic ARN_ field and choose the ARN that pops up, that belongs to the topic you created some steps ago, **PacketCaptureProcessorTopic**.
 * From the _Protocol_ dropdown, select **HTTP**.
 * In the endpoint text field, enter: **http://|DNS-name-of-your-ELB|/update**, where |DNS-name-of-your-ELB| is the DNS name you used to check the website above.

Click on the _Create subscription_ button.

![sns_sub_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_3.png "")

You will be taken to this screen. We need to go to the list of subscriptions. Click on the _Subscription_ item on the sidebar to the left.

![sns_sub_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_4.png "")

From the list, select the subscription you jusut created, and click on the _Request confirmation_ button above.

![sns_sub_5](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_5.png "")

Now we just need to verify this subscription for SNS to be able to start sending events to it.

## Verify SNS subscription

We are very close to seeing the whole workflow in action! We need to get hold of the token that was sent to this endpoint to do the verification.

You can retrieve this token by calling the **http://|DNS-name-of-your-ELB|/get-token** endpoint from your browser. Since the token has been sent only once so far, only one of the servers behind your load balancer will have it. If you see a message that says «_Not on this server_», then keep refreshing until you get the token. It should look like this:

![sns_sub_5b](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_5b.png "")

Back to the SNS console, still in the Subscriptions screen, click on the _Confirm subscription_.

![sns_sub_5](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_5.png "")

When the confirmation dialog pops up, enter the token you have just retrieved from the **get-token** endpoint, and click on the  _Confirm subscription_.

![sns_sub_6](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/sns_sub_6.png "")

**Note**: If, by accident, you submitted the verification token more than once, you can try refreshing until one of the tokens you receive works. There can be, at most, two tokens.

## Upload file

In the search box on the _Services_ menu, enter _S3_ and then click on the _S3_ service link.

![s3_1](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/s3_1.png "")

Find the bucket that has been created for you (starting with **viw-lambda-ec2-lab**) and click on its name.

![s3_2](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/s3_2.png "")

Click on the _Upload_ button to upload a sample file. You can use any of the provided **.cap** files in the _captures_ directory in this repository.

![s3_3](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/s3_3.png "")

Click on the _Add files_ button to add files to the upload list.

![s3_4](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/s3_4.png "")

Now click on the _Upload_ button to start the upload process.

![s3_5](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/s3_5.png "")

Within a few seconds, refresh the contents of the bucket by using the refresh _icon_ on the right side of the screen. You should see a _csv_ prefix created. You can click this, and you will see one or more CSV files (depending on how many capture files you uploaded). These contain part of the contents of the capture files dumped as a CSV file.

![s3_6](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/s3_6.png "")

## Check DynamoDB table and website again

From the _Services_ menu, choose _DynamoDB_ and click it.

![dynamo_0](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/dynamo_create_0.png "")

Now, click on the sidebar to your left on the _Tables_ item, and then choose the _Items_ tab at the right of the screen. You will now see that the data in the capture file has also been uploaded to DynamoDB.

![dynamo_data](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/dynamo_data.png "")

Finally, take a look at the website using the DNS name of the ELB as the URL.

For every file processed, an SNS notification has been sent to the endpoint living in the two EC2 instances. Depending on the instance to which the load balancer decided to route the traffic, you may encounter that one of the instances has changed state, while the other has not.

If the instance received the notification, you will see the following:

![website_updated](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/basics-part-2/img/website_updated.png "")

## Congratulations! You have made it to the end of this lab.

By now, you should have gained more insight on:
 * How event-driven architectures can be implemented using Lambda, SNS and events.
 * How to create EC2 instances from scratch and initialize them using user data.
 * How to place EC2 instances behind a load balancer.
 * How to reuse code in Lambda functions by placing it into a Lambda layer.
 * How to create and query a DynamoDB table from the console.

## Data source

Capture files were obtained from: https://wiki.wireshark.org/SampleCaptures
