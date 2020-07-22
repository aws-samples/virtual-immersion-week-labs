
# LAB 01 Launch a new Windows EC2 instance and add a new Drive

## 0. Before your start

- 0.1. Login to the AWS Console
- 0.2. Make sure you are in the "Ireland" region.

## 1. Create a new key pair

- 1.1. Got to the `EC2` service
- 1.2. Look for `Network and Security` in the menu on the left and click on `Key Pais`
- 1.3. Click on `Create key pair`
- 1.4. Name your key "asademo", use the "pem" format and click on `Create key pair`
- 1.5. Congratulations! You should now have a new prive key called "asademo.pem" in your Downloads folder

## 2. Launch an EC2 instance

- 2.1. Got to the `EC2` service
- 2.2. Click on `Launch Instance`
- 2.3. Search for "Windows" in the AMI search box
- 2.4. Step 1: Choose an Amazon Machine Image (AMI): Look for the AMI "Microsoft Windows Server 2019 Base - ami-0753ddff1a67fca78" and click `Select`
- 2.5. Step 2: Choose an Instance Type: Choose the "t2.large" instance and click `Next: Configure Instance Details`
- 2.6. Step 3: Configure Instance Details: Enable "T2/T3 Unlimited" and click `Next: Add Storage`
- 2.7. Step 4: Add Storage: Enable Encryption by choosing the AWS managed key called 'aws/ebs' and click `Next: Add Tags`
- 2.8. Step 5: Add Tags: Add a "Name" tag and call it "MyLabServer" make sure Instances and Volumes are tagged and click `Next: Configure Security Group`
- 2.9. Step 6: Configure Security Group: Create a new security group that allows TCP 3389 from anywhere (0.0.0.0/0) and click `Revew and Launch`
- 2.10. Review all the defaults and click `Launch`
- 2.11. Choose your existing Key and check the checkbox at the bottom and click `Launch Instance`
- 2.12. Congratulations! You have launched a Windows EC2 Instance

## 3. Login to the EC2 instance (Windows)

- 3.1. Got to the `EC2` service
- 3.2. Click on `Running instances`
- 3.3. Click on the intance id and then click on `Actions -> Get Windows Password`
- 3.4. Choose the public key "asademo" and click `Decrypt Password`
- 3.5. Note the public DNS, user name and password (be careful with trailing spaces)
- 3.6. Open a remote desktop client. You can search for `Remote Desktop Connection` or Click the `Start` button and type `Run` and run `mstsc.exe`
- 3.7. Click on the `Show Options` button at the bottom
- 3.8. Type the Public DNS that you got from section 2 under "Computer" and use "Administrator" for the user name and then click `Connect`
- 3.9. Type the password that you got from section 2 and click `OK`
- 3.10. Congratulations! You have connected to your EC2 Instance

## 4. Create a new EBS Volume

- 4.1. Got to the `EC2` service
- 4.2. Look for `Elastic Block Store` in the menu on the left and click on `Volumes`
- 4.3. Create `Create Volume`
- 4.4. Create a new General Purpose SSD volume, 30 GB in size. Make sure it is created in the same Availability Zone as your EC2 instance, that the volume is encrypted with AWS managed keys and that is labeled to match your existing EC2 instance and volumes
- 4.5. Click on your newly created volume and choose Actions -> Attach Volume
- 4.6. Select the instance "MyLabServer" and use "xvdf" as for the device name

## 5. Detect, Format and Mount a new EBS Volume

- 5.1. Login to your Windows EC2 instance
- 5.2. Open the Disk Management tool. You can search for `Create and format hard disk partitions` or Click the `Start` button and type `Run` and run `diskmgmt.msc`
- 5.3. Click Actions -> Rescan Disks. You should see a new disk appear under "Disk 0"
- 5.4. Right click on `Disk 1` and click `Online`
- 5.5. Right click on `Disk 1` and click `Initialize Disk`
- 5.6. Verify that `Disk 1` is selected and that the partition style is `MBR` and Click `OK`
- 5.7. Right click on the "100.00 GB Unallocated" Space and select `New Simple Volume`
- 5.8. Go though the New Simple Volume Wizard. Use all the space available to create a new NTFS Quick formated "D:" drive.
- 5.9. Congratulations! You have mounted a new drive.
