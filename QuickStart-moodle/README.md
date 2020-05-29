### Quickstart - Install a single-node Moodle on AWS

> Setup a single-node Moodle LMS on an EC2 instance behind an ElasticLoad Balancer with HTTPS. This setup can be used as a starting point and system administrators can choose to scale 'up' or 'out' by increasing the instance size, adding more instances or hosting the database in a managed database service like Amazon RDS etc. The approximate monthly cost of this setup less than $2/day.

#### Basic Setup

1. Start a t3.medium instance (2vCPU, 4GB RAM), open ports should be TCP 80 and TCP 22, write down the instance id
2. Create a certificate in ACM
3. Create a Target Group and add the EC2 instance using port 80 and '/test.html' for test page
4. Create Application Load Balancer. Add a listener on port 443 that points to the Target Group created in step 3 and use the certificate in created in step 2. Add another listener in port 80 and set it to 'Redirect to...'  HTTPS, port 443
5. Create Route53 A record an point it to the ELB alias
6. Install Apache & MySQL on the EC2 instance. 
```
sudo yum update -y
sudo amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
sudo yum install -y httpd mariadb-server git php-xml php-xmlrpc php-gd php-intl php-mbstring php-soap php-opcache
sudo systemctl start httpd
sudo systemctl enable httpd
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo usermod -a -G apache ec2-user
exit
```
7. Log back in to your EC2 instance and configure MySQL, create a user and a database
```
sudo mysql_secure_installation
mysql -u root -p
CREATE DATABASE moodle;
CREATE USER 'moodle-user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON moodle.* TO 'moodle-user'@'localhost';
FLUSH PRIVILEGES;
exit
```
8. Change permisions
```
sudo chown -R ec2-user:apache /var/www
sudo chmod 2775 /var/www && find /var/www -type d -exec sudo chmod 2775 {} \;
find /var/www -type f -exec sudo chmod 0664 {} \;
```
9. Create a test page for the load balancer
```
echo "OK" > /var/www/html/test.html
```
10. STOP and check that HTTPS is functional by navigating to your domain name
11. Download & install Moodle. 
```
git clone -b MOODLE_38_STABLE git://git.moodle.org/moodle.git
cp -r moodle/* /var/www/html/
sudo mkdir /var/www/moodledata
sudo chown -R apache /var/www/moodledata
```
12. Open a web brower window and navigate to your EC2 DNS using HTTP (i.e. http://ec2-1-1-1-1.eu-west-1.compute.amazonaws.com/) 
13. Once the installation is complete, modify the configuration file /var/www/html/config.php by replacing the contents of "$CFG->wwwroot" and adding "$CFG->sslproxy=true;"
```
vi /var/www/html/config.php
```
14. Modify the security group from the EC2 instance to only allow traffic to come in from the ELB
15. Done! You can now navigate to your Moodle instance by using your domain name via HTTPS.

#### Next Steps 

1. Regularly backup your EC2 instance by using AWS Backups
2. Improve network security by making your existing subnet private, add a public subnet plus a NAT Gateway and reconfigure the Elastic Load Balancer to work with the newly provisioned public subnet

#### Scaling and High Availability

1. To reduce management overhead and to increase database availability; migrate the database to Amazon RDS and enable Multi-AZ
2. To increase availability of the application; Move data in '/var/www/moodledata' to a shared network storage like Amazon Elastic File System (Amazon EFS) and add additional instances to the Target Group 
3. Increase performance by adding a cache layer; you can host the Moodle Redis cache store in Amazon ElastiCache
