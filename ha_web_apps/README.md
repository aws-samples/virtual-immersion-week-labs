# Highly Available Web Applications Lab
*Compute Series - Virtual Immersion Weeks*

## Objective

The objective of this lab is to give you hands-on experience in building highly-available, scalable web applications on AWS. You will deploy a backend application onto a group of Amazon EC2 instances, store a static frontend application in Amazon S3, and will place these behind Amazon CloudFront to leverage the benefits of DDoS mitigation provided by AWS Shield.

## Architecture

<p align="center">
    <img alt="architecture_diagram" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/architecture_diagram.png" width="85%">
</p>

## Steps

So that you may concentrate on learning about the services on which this laboratory focuses, the underlying network has been configured for you. This includes the VPC, public and private subnets, the Internet Gateway and the NAT Gateways for each availability zone.

Let's start by configuring a bastion host, with which you will be able to connect to the application instances later on.

### Configuration of the bastion host

In this first step, we will launch a bastion host in one of the public subnets.

 1. In the search box in the Services menu at the top left corner of your browser, type in **EC2** and click on the **EC2** service.

<p align="center">
    <img alt="bastion_launch_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_0.png" width="85%">
</p>

 2. This will take you to the main EC2 console. There, click on the *Launch Instance* button to start the creation process.

<p align="center">
    <img alt="bastion_launch_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_1.png" width="85%">
</p>

 3. The first screen that will be presented to you lets you choose the AMI (Amazon Machine Image) that will be used to initialize your root volume. This image contains the operating system, and may (or may not) contain other software packages and tools. In this lab, we will use a vanilla Amazon Linux 2 image: *Amazon Linux 2 AMI (HVM), SSD Volume Type*. Make sure the target architecture is *x86*. Click on the *Select* button to the right of the name to select it.

<p align="center">
    <img alt="bastion_launch_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_2.png" width="85%">
</p>

4. Now, we need to choose the type of instance we want for our bastion host. In this case, we will choose a **t2.micro** instance. Click on the checkbox to select the instance, if not already selected, and click on the *Next: Configure Instance Details* button to continue.

<p align="center">
    <img alt="bastion_launch_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_3.png" width="85%">
</p>

5. Now it's time to configure the instance details, which includes the network (VPC) and subnet in which this instance will be launched, whether it will be automatically assigned an IP address, its behavior upon shutdown, and other related settings.
<br/>
<br/>
Choose the VPC that has been created for you, **ImmersionWeekLabVPC**, and the public subnet of your choice. The rest of the settings can be left as they are. In this case, as an additional setting, the *Shutdown behavior* has been set to **Terminate**.
<br/>
<br/>
Click on **Next: Add Storage** to continue.

<p align="center">
    <img alt="bastion_launch_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_4.png" width="85%">
</p>

6. Now it's time to add storage to your instance. This instance is going to be used purely as a bastion host. Thus, there is no need to allocate any extra space than the 8 GiB already set by default.
<br/>
<br/>
Leave things as they are and click on **Next: Add Tags**.

<p align="center">
    <img alt="bastion_launch_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_5.png" width="85%">
</p>

7. The next thing to do is to add tags to the instance to help identify it among other resources. In this case, it is safe to just continue.
<br/>
<br/>
Click on *Next: Configure Security Group* to continue.

<p align="center">
    <img alt="bastion_launch_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_6.png" width="85%">
</p>

8. It is necessary to define what network traffic will be allowed in and out of the instance. For a bastion host, having TCP por 22 (SSH) open to a reduced range of IP addresses should suffice for most use cases. In this case, the port is open to any IPv4 address to simplify the configuration during the workshop.
<br/>
<br/>
Make sure that only the **ImmersionWeekBastionSG** Security Group is selected, and then click on the *Review and Launch* button at the bottom right corner.

<p align="center">
    <img alt="bastion_launch_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_7.png" width="85%">
</p>

9. Before launching the instance, make sure all information is correct in the Review screen. Once you are done, click on the *Launch* button at the bottom right corner of the screen.

<p align="center">
    <img alt="bastion_launch_8" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_8.png" width="85%">
</p>

10. As a final step, you need to either select an existing key pair, or create a new key pair to be able to connect to the instance.
<br/>
<br/>
From the first dropdown menu, choose **Create a new key pair**, and enter the name **BastionHost** in the *Key pair name* textbox, then click on the *Download Key Pair* to download it.
<br/>
<br/>
Now click on the *Launch Instances* button. Your instance is now being launched.

<p align="center">
    <img alt="bastion_launch_9" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/bastion_launch_9.png" width="85%">
</p>

### Launch Template setup

While waiting for the bastion host to launch, you can start creating a Launch Template for your application server instances.

A *Launch Template* is a resource that enables you to store launch parameters so that you do not have to specify them every time you launch an instance. In this case, all application servers are to be launched of the same type and running the same initialization script.

Additionally, and unlike their ancestors, *Launch Configurations*, Launch Templates can be versioned, and specific versions can be referenced from different resources within AWS.

1. While still in the EC2 console, click on the **Launch Templates** menu item on the left sidebar, under *Instances*.

<p align="center">
    <img alt="launch_template_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_1.png" width="25%">
</p>

2. Click on the **Create launch template** button in the middle of the screen.

<p align="center">
    <img alt="launch_template_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_2.png" width="85%">
</p>

3. Once in the Launch Template parameter screen, start by entering a name for the new template. In this case, we will use **ImmersionWeekAppServerLT**. Optionally, you can enter a description of this version of your template in the *Template version description* input box.

<p align="center">
    <img alt="launch_template_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_3.png" width="85%">
</p>

4. From the *AMI* dropdown, choose the **Amazon Linux 2 AMI (HVM), SSD Volume Type** AMI.

<p align="center">
    <img alt="launch_template_3a" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_3a.png" width="55%">
</p>

5. From the *Instance type* dropdown, choose the **t3.micro** instance type. You can type in the name (or part of it) to make your search easier.

<p align="center">
    <img alt="launch_template_3b" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_3b.png" width="55%">
</p>

6. From the *Key pair name* dropdown, choose the **BastionHost** key pair. For the sake of simplicity, the same key pair for both the bastion host and the application instances will be used.

<p align="center">
    <img alt="launch_template_3c" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_3c.png" width="55%">
</p>

7. From the *Security groups* dropdown, choose the **ImmersionWeekAppInstancesSG** security group. This Security Group has been created for you, and allows inbound traffic only from resources in the **ImmersionWeekLoadBalancerSG** Security Group, which will later be associated to the Application Load Balancer (ALB).

<p align="center">
    <img alt="launch_template_3d" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_3d.png" width="55%">
</p>

8. At the bottom of the screen, you will find the *Advanced details* section. Click on it to reveal the contents of this section.

<p align="center">
    <img alt="launch_template_3e" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_3e.png" width="55%">
</p>

9. In order for these instances to have the necessary packages automatically installed, they need to run an initialization script. Shell script scan be run by means of the *User data* instance parameter. In this case, the script will update the packages to their latest version by means of the *yum* package manager, and will then install an Apache 2 web server, and a simple Python application.
<br/>
<br/>
Open the **userdata.sh** file in your Cloud9 environment, and copy the contents into the *User data* text area. 

```sh
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
```

Now click on the *Create launch template* button to create the Launch Template.

<p align="center">
    <img alt="launch_template_3f" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_3f.png" width="55%">
</p>

10. You should be taken to a screen like the one below. You can simply click on the *Create Auto Scaling group* link, or go back to the EC2 console.

<p align="center">
    <img alt="launch_template_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/launch_template_4.png" width="85%">
</p>

### Auto-Scaling group setup

Having the Launch Template is just the beginning. Not only is it necessary to spin up the application servers, but it is also necessary to make sure there are is the desired number of them and, eventually, that this number increases or decreases based on the current load on the servers. This is what an *Auto Scaling Group* is for.

1. If you are entering the Auto Scaling Group console from the EC2 console, click on the *Auto Scaling Groups* menu item from at bottom left side of the screen. If you just clicked on the link from the last step, you may safely jump to step 2.

<p align="center">
    <img alt="asg_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_1.png" width="25%">
</p>

2. Make sure you open the new console.

<p align="center">
    <img alt="asg_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_0.png" width="85%">
</p>

3. Click on the *Create Auto Scaling group* button in the middle of the screen.

<p align="center">
    <img alt="asg_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_2.png" width="85%">
</p>

4. The first thing to do is giving this new Auto Scaling Group (ASG) a name. In the *Auto Scaling group name* box, enter **ImmersionWeekASG**.
<br/>
<br/>
Then, it is necessary to choose is the Launch Template or Launch Configuration to use, that will tell the ASG how to launch new instances. From the *Launch template* dropdown, select the **ImmersionWeekAppServerLT** template.
<br/>
<br/>
Then, click on *Next* to continue.

<p align="center">
    <img alt="asg_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_3.png" width="85%">
</p>

5. It is now necessary to choose in which VPC and what subnets will the ASG launch the newly created instances. Application servers should only be reachable either from the load balancer or the bastion host, so the isolation of a private subnet is desired.
<br/>
<br/>
From the *VPC* dropdown, choose the **ImmersionWeekLabVPC** VPC. Then, choose the **ImmersionWeekLabVPC-private-a** and **ImmersionWeekLabVPC-private-b** subnets from the *Subnets* dropdown below.
<br/>
<br/>
Click on *Next* to continue.

<p align="center">
    <img alt="asg_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_4.png" width="85%">
</p>

6. Load balancing could be configured directly from this screen. However, in order to explore the EC2 console in greater detail, load balancing is going to be configured separately.
<br/>
<br/>
Click on the *Next* button to continue.

<p align="center">
    <img alt="asg_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_5.png" width="85%">
</p>

7. Two instances are needed for this lab: one in each availability zone. Thus, all minimum, desired, and maximum capacity should be set to 2.
<br/>
<br/>
Leave the rest of the configuration parameters as they are, and click on the *Next* button at the bottom right corner of the screen to continue.

<p align="center">
    <img alt="asg_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_6.png" width="85%">
</p>

8. No notifications will be set during this lab. Click the *Next* button at the bottom right corner of the screen to continue.

<p align="center">
    <img alt="asg_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_7.png" width="85%">
</p>

9. No tags will be set for this ASG, either. Click the *Next* button at the bottom right corner of the screen to continue.

<p align="center">
    <img alt="asg_8" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_8.png" width="85%">
</p>

10. Scroll down to the bottom of the screen and click the *Create Auto Scaling group* button to create the ASG.

<p align="center">
    <img alt="asg_9" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/asg_9.png" width="85%">
</p>

### Target group setup

By now, the ASG you created in the previous section should already be launching the instances it needs to achieve the desired capacity of 2. In the meantime, you will configure a new resource, a *target group*.

Target groups are groups of instances that act, just as the name says, as *targets* for the load balancer. When the load balancer receives a request, it chooses an instance from its assigned target group and sends the request to that instance.

1. To create a target group, go to the EC2 console and click on the *Target Groups* menu item on the sidebar to your left, just below the *Load Balancers* item.

<p align="center">
    <img alt="target_groups_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/target_groups_1.png" width="25%">
</p>

2. Click on the *Create target group* button on the left side of the screen.

<p align="center">
    <img alt="target_groups_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/target_groups_1b.png" width="85%">
</p>

3. In the *Target group name* text box, enter **ImmersionWeekTargetGroup**. Then, make sure to select the **ImmersionWeekVPC** VPC from the *VPC* dropdown.

<p align="center">
    <img alt="target_groups_2a" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/target_groups_2a.png" width="85%">
</p>

4. Click on *Advanced health check settings* to reveal some additional health check parameters. To speed up matters a bit, set the *Healthy threshold* to 3. This is the number of times that a target should appear healthy to the load balancer before it is considered to be in the **healthy** state.
<br/>
<br/>
In this case, reducing the number from 5 to 3 will make the load balancer consider the instances healthy within a shorter timespan.
<br/>
<br/>
Click on the *Next* button at the bottom right corner of the screen to continue.

<p align="center">
    <img alt="target_groups_2b" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/target_groups_2b.png" width="85%">
</p>

5. Now review the information, and click on the *Create target group* button at the bottom right corner of the screen.

<p align="center">
    <img alt="target_groups_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/target_groups_3.png" width="85%">
</p>

### Load balancer setup

Everything is ready to set up the load balancer. From the EC2 console, click on the *Load Balancers* menu item on the left sidebar.

<p align="center">
    <img alt="load_balancer_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_1.png" width="25%">
</p>

1. Once in the *Load Balancer* console, click on the *Create Load Balancer* button.

<p align="center">
    <img alt="load_balancer_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_2.png" width="85%">
</p>

2. Select the *Application Load Balancer* by clicking on the *Create* button inside the *Application Load Balancer* section.

<p align="center">
    <img alt="load_balancer_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_3.png" width="85%">
</p>

3. Start by naming your load balancer **ImmersionWeekALB**.
<br/>
<br/>
In order to be reachable from the internet and by CloudFront, you need to create an *internet-facing* ALB. Thus, leave the *Scheme* radio buttons as they are. The ALB will not be handling any incoming IPv6 traffic, either, so you can simply leave the *IP address type* dropdown selection as **ipv4**.
<br/>
<br/>
Listeners should be left as they are, since the ALB will only listen to incoming traffic from CloudFront on port 80.
<br/>
<br/>
Choose the **ImmersionWeekVPC** from the *VPC* dropdown, check both availability zones, and select both public subnets, **ImmersionWeekLabVPC-public-a** and **ImmersionWeekLabVPC-public-b** from the corresponding dropdowns.
<br/>
<br/>
Scroll down and click the *Next: Configure Security Settings* button to continue at the bottom right corner of the screen.

<p align="center">
    <img alt="load_balancer_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_4.png" width="85%">
</p>

4. For the sake of simplicity, no secure listener is going to be configured for this load balancer in this lab, so you may safely skip this step by clicking on the *Next: Configure Security Groups* button at the bottom right corner of the screen.

<p align="center">
    <img alt="load_balancer_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_5.png" width="85%">
</p>

5. Click on *Select an existing security group*, and make sure that the only group selected is **ImmersionWeekLoadBalancerSG**. Then, click on the *Next: Configure Routing* to continue.

<p align="center">
    <img alt="load_balancer_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_6.png" width="85%">
</p>

6. From the *Target group* dropdown, choose **Existing target group**, and choose the **ImmersionWeekTargetGroup** from the *Name* dropdown. Leave the rest as is, and click on the *Next: Register Targets* at the bottom right corner of the screen to continue.

<p align="center">
    <img alt="load_balancer_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_7.png" width="85%">
</p>

7. Targets (instances) will automatically be registered by the ALB once the configuration process has been completed, so you may safely click on the *Next: Review* button at the bottom right corner of the screen to continue.

<p align="center">
    <img alt="load_balancer_8" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_8.png" width="85%">
</p>

8. At this step, you may review whether the configuration parameters for this ALB are correct. Once you are sure, click on the *Create* button at the bottom right corner of the screen.

<p align="center">
    <img alt="load_balancer_9" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_9.png" width="85%">
</p>

If successful, you should be taken to this screen. Click on the *Close* button to continue.

<p align="center">
    <img alt="load_balancer_10" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/load_balancer_10.png" width="85%">
</p>

### Associate the target group to the Auto Scaling group.

Go back to the Auto Scaling Groups console by clicking on the *Auto Scaling Groups* menu item at the bottom left side of the screen.

Once in the Auto Scaling Groups console, click on the **ImmersionWeekASG** auto scaling group then, in the bottom pane, scroll down until you reach the *Load balancing* section. Click on the *Edit* button inside this section.

<p align="center">
    <img alt="target_group_asg_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/target_group_asg_1.png" width="85%">
</p>

Click on the *Choose a target group for your load balancer* dropdown, and choose the **ImmersionWeekTargetGroup**, then click on the *Update* button to continue.

<p align="center">
    <img alt="target_group_asg_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/target_group_asg_2.png" width="85%">
</p>

Now, your load balancer and application servers should be ready to respond to incoming traffic.

### Checkpoint One - Make sure the web application works

It's time to test the application. Go to the load balancer console by clicking on the *Load balancers* menu item on the left side of the screen in the EC2 console. Then, select your recently created load balancer, **ImmersionWeekALB**.

In the bottom pane, in the *Description* tab, you should see load balancer parameters just like in the image below.

<p align="center">
    <img alt="elb_app_check_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/elb_app_check_1.png" width="85%">
</p>

Copy the *DNS name* from the ALB information and paste it in a browser. You should see something like this:

<p align="center">
    <img alt="elb_app_check_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/elb_app_check_2.png" width="85%">
</p>

If you keep refreshing, you should see that two availability zone names are being alternately returned. If so, both your ALB and your application servers are running fine, and you may proceed to the next step.

In case the service is still unavailable, make sure the ALB is already active, and not in the *provisioning* state.

### Create a CloudFront distribution for your backend

It is time to create a CloudFront distribution to place in front of your ALB.

1. Click on the *Services* menu at the top left side of the screen, then enter *cloudfront* in the search box and click on the *CloudFront* service menu item.

<p align="center">
    <img alt="cloudfront_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cloudfront_0.png" width="85%">
</p>

2. Click on the *Create Distribution* button.

<p align="center">
    <img alt="cloudfront_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cloudfront_1.png" width="85%">
</p>

3. Under *Web*, click on the *Get Started* button.

<p align="center">
    <img alt="cloudfront_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cloudfront_2.png" width="85%">
</p>

4. Click on *Origin Domain Name* text box. A number of resources should appear. Make sure to scroll down until you find your ALB resource, then select it. This should also populate the *Origin ID* field.
<br/>
<br/>
Select **TLSv1.2** from the *Minimum Origin SSL Protocol* options, then **Redirect HTTP to HTTPS** from the *Viewer Protocol Policy*, and **GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE** from the *Allowed HTTP Methods* options.

<p align="center">
    <img alt="cloudfront_3a" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cloudfront_3a.png" width="85%">
</p>

Your ALB resource should look like this.

<p align="center">
    <img alt="cloudfront_3b" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cloudfront_3b.png" width="85%">
</p>

5. The rest should be left as is, as the following to screenshots show.

<p align="center">
    <img alt="cloudfront_3c" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cloudfront_3c.png" width="85%">
</p>

6. After having scrolled down to the bottom of the window, click the *Create Distribution* button at the bottom right corner of the screen.

<p align="center">
    <img alt="cloudfront_3d" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cloudfront_3d.png" width="85%">
</p>

Your frontend CloudFront distribution is now being created. Take note of the domain name in the *Domain Name* column, and continue to the next section.

### Modify your frontend application to point to the backend Cloudfront domain.

Among the assets you decompressed at the beginning of this laboratory, there is an **index.html** file, which contains a very simple piece of code to query the backend. For it to point to the right domain, you need to modify it and enter the CloudFront domain that you just wrote down.

Open the file and look for the *backendCfDistribution* variable, and change its value to the correct domain name.

<p align="center">
    <img alt="index_html_modification" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/index_html_modification.png" width="55%">
</p>

The final string should look like: **https://a1bc23def4g5hi.cloudfront.net**

### Create an S3 bucket for static content.

The backend is running. It is time to deploy the frontend. For that purpose, a very simple application has been put together for you. All it does is, whenever it runs, it fetches the value returned by the backend and prints its browser screen.

The application is just an HTML file, so it can be served from S3 through CloudFront. CloudFront, in turn, will handle the caching of the HTML file in the edge, so that users of your application always get it from a point that results in the fastest delivery of content.

1. Start by clicking on the *Services* menu at the top left corner of the console, and type in *S3* in the search bar, then click on the *S3* service menu item.

<p align="center">
    <img alt="s3_0" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_0.png" width="55%">
</p>

2. Enter the name of your bucket. For this lab, you will use a name composed by **immersion-week-static-content-** followed by your account number. In this case, a fake account number of **012345678901** has been used.
<br/>
<br/>
The name of the bucket, among other symbols, *cannot contain uppercase characters*. For the region, choose **eu-west-1**.
<br/>
<br/>
Click on the *Create bucket* button to continue.

<p align="center">
    <img alt="s3_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_1.png" width="65%">
</p>

3. Once created, you will be taken to the bucket page. Click on the *Upload* button.

<p align="center">
    <img alt="s3_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_2.png" width="85%">
</p>

4. Click on the *Add files* button to upload your application files, and pick the **index.html** and **jquery-3.5.1.min.js** files from your hard disk.

<p align="center">
    <img alt="s3_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_3.png" width="85%">
</p>

5. You should see these two files in the list of files to upload as follows. Click on the *Upload* button to upload them.

<p align="center">
    <img alt="s3_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_4.png" width="85%">
</p>

6. You should now see your files in the S3 bucket.

<p align="center">
    <img alt="s3_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_5.png" width="85%">
</p>

7. Now click on the *Properties* tab in your S3 bucket screen, and click on the *Static website hosting* card.

<p align="center">
    <img alt="s3_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_6.png" width="85%">
</p>

8. Select the *Use this bucket to host a website* radio button and, as index document, enter **index.html**. Click *Save* to enable the static website hosting feature.

<p align="center">
    <img alt="s3_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/s3_7.png" width="55%">
</p>

### Create a CloudFront distribution for your frontend

This is the last part of this lab. You are just a single step away of serving your application entirely through CloudFront.

1. Once again, choose the CloudFront service from the *Services* menu at the top left corner of the screen. Once in the CloudFront console, click on the *Create Distribution* button.

<p align="center">
    <img alt="cf_s3_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cf_s3_1.png" width="85%">
</p>

2. Click on the *Origin Domain Name* text box and look among your available S3 origins the one that belongs to your recently created bucket, then click on it.
<br/><br/>
***Warning***: CloudFront automatically populates this textbox as *bucketname.s3.amazonaws.com*, a value that is only valid for buckets in the *us-east-1* location. You need to correct the domain name so that it looks like *bucketname.s3.region-name.amazonaws.com*. In this case, for example, it would look like: *immersion-week-static-content-012345678901.s3.eu-west-1.amazonaws.com*.
<br/><br/>
From *Restrict Bucket Access*, choose **Yes**. This will display the *Origin Access Identity*, *Comment*, and *Grant Read Permisions on Bucket* fields. Make sure you set them to **Create a New Identity**, **immersion-week-access-identity**, and **Yes, Update Bucket Policy** respectively.

<p align="center">
    <img alt="cf_s3_2a" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cf_s3_2a.png" width="85%">
</p>

3. You can leave the rest as is, like in these screenshots.

<p align="center">
    <img alt="cf_s3_2b" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cf_s3_2b.png" width="85%">
</p>

4. Finally, click on the *Create Distribution* button to create your frontend distribution.

<p align="center">
    <img alt="cf_s3_2c" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cf_s3_2c.png" width="85%">
</p>

5. Your CloudFront distributions should now look like these.

<p align="center">
    <img alt="cf_final" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/cf_final.png" width="85%">
</p>

### Testing the application

Open a new tab in your browser and navigate to the *index.html* in the frontend domain, the address being something like: *https://a12bcd34efg8h.cloudfront.net/index.html* You should get a result like this:

<p align="center">
    <img alt="result" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/result.png" width="85%">
</p>

If you have, congratulations! You made it to the end of the lab.

### **Bonus** - Connecting to the application servers using the bastion host.

You can connect to the application servers using ssh and the bastion host.

First, copy the *.pem* file that you downloaded at the beginning of the lab to the bastion host by using the *scp* command:
```
# scp -i BastionHost.pem BastionHost.pem ec2-user@<bastion-host-ip>:/home/ec2-user/
```

Then, using the same key file, connect to the EC2 instance.

```
# ssh -i BastionHost.pem ec2-user@<bastion-host-ip>
```

where *<bastion-host-ip>* is the public IP that has been assigned to your bastion host. You can find it in the EC2 console, either in the bottom pane in the *Description* tab, *IPv4 Public IP* field on the right:

<p align="center">
    <img alt="ec2_ipv4_public_ip_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/ec2_ipv4_public_ip_1.png" width="85%">
</p>

Or in the instance description in the top pane:

<p align="center">
    <img alt="ec2_ipv4_public_ip_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/ec2_ipv4_public_ip_2.png" width="85%">
</p>

Once logged into the bastion host, use the uploaded key file and the private IPv4 address of the application server to log into it:

```
# ssh -i BastionHost.pem <app-server-ip>
```

You can find the private IP of either app server by checking either the top or bottom pane of the EC2 console, next to the *Private IPs* field.

Finally, test the web application running on this server by using *curl*:

```
curl localhost
```

You should see something like this:

<p align="center">
    <img alt="app_server_curl" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/ha_web_apps/img/app_server_curl.png" width="85%">
</p>
