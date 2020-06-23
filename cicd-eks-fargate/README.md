
### Download and install dependencies

#### Download and install jq.

```
sudo yum -y install jq
```

Before creating the cluster, you need to install both the **kubectl** and **eksctl** command-line tools.

#### Download and install kubectl

Download the Amazon EKS-vended **kubectl** binary.

```
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/linux/amd64/kubectl
```

Apply execute permissions to the binary.

```
chmod +x ./kubectl
```

Copy the binary to a folder in your **PATH**.

```
sudo mv kubectl /usr/local/bin
```

Test your recently installed version of **kubectl**.

```
kubectl version --short --client
```

#### Download and install aws-iam-authenticator

```
curl -o aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/linux/amd64/aws-iam-authenticator
```

```
chmod +x ./aws-iam-authenticator
```

```
sudo mv aws-iam-authenticator /usr/local/bin
```

#### Download and install eksctl

```
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
```

```
sudo mv /tmp/eksctl /usr/local/bin
```

```
eksctl version
```

#### Create and attach an IAM role to your Cloud9 instance.

Click on the following [deep link](https://console.aws.amazon.com/iam/home#/roles$new?step=review&commonUseCase=EC2%2BEC2&selectedUseCase=EC2&policies=arn:aws:iam::aws:policy%2FAdministratorAccess) to open the IAM console and create a new role with Administrator access for your instance.

Make sure that the *AWS service* and *EC2* options are selected, then click *Next* to view permissions.

Make sure that **AdministratorAccess** is checked, then click *Next* to review.

Enter *eks-cloud9-admin* as the role name, and click *Create role*.

#### Assign the newly created IAM role to your Cloud9 instance.

Click on the following [deep link](https://console.aws.amazon.com/ec2/v2/home?#Instances:tag:Name=aws-cloud9-MyCloud9Environment*;sort=desc:launchTime) to open the EC2 console and find your Cloud9 instance.

Click on *Actions*, select *Instance Settings*, and click *Attach/Replace IAM Role*.

From the *IAM role* dropdown, select the **eks-cloud9-admin** role, and click on *Apply*.

#### Configure Cloud9 to use the newly assigned role.

Click on the gear at the top right corner, then click on *AWS Settings*, and disable the *AWS managed temporary credentials* option.

Erase the credentials that may be cached in the Cloud9 environment.

```
rm -vf ${HOME}/.aws/credentials
```

Configure the AWS CLI with the current region:

```
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
echo "export AWS_REGION=${AWS_REGION}" >> ~/.bash_profile
aws configure set default.region ${AWS_REGION}
aws configure get default.region
```

Make sure Cloud9 is using the **eks-cloud9-admin** role that we created.

```
INSTANCE_PROFILE_NAME=`basename $(aws ec2 describe-instances --filters Name=tag:Name,Values=aws-cloud9-${C9_PROJECT}-${C9_PID} | jq -r '.Reservations[0].Instances[0].IamInstanceProfile.Arn' | awk -F "/" "{print $2}")`
aws iam get-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME --query "InstanceProfile.Roles[0].RoleName" --output text
```

The output should be the name of the role, **eks-cloud9-admin**.


### Create the EKS cluster

Generate an SSH key in Cloud9.

```
ssh-keygen
```

Upload the public key to your EC2 region.
```
aws ec2 import-key-pair --key-name "ekslab" --public-key-material file://~/.ssh/id_rsa.pub
```


```
eksctl create cluster --name ekslabcluster --version 1.16 --region eu-west-1 --full-ecr-access --fargate
```

Cluster provisioning takes approximately between 10-15 minutes. When complete, test that your **kubectl** configuration is correct.

```
kubectl get svc
```

You should see something like this:

```
NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
```
