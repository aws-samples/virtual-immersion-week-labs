## Deploying applications to Amazon EKS and AWS Fargate with a CI/CD pipeline based on AWS CodeBuild.

### Objective

The objective of this lab is to show you how to build a simple CI/CD pipeline that deploys containerized applications to Amazon EKS by using AWS CI/CD services such as AWS CodePipeline and AWS CodeBuild.

### Before you begin

Please make sure that you are working within the region that your instructor has told you to. Failure to do so could result in the laboratory not working as expected.

### Create a AWS Cloud9 environment

Click on the Services menu at the top left corner of the screen, and enter **Cloud9** into the search bar, then click on the *Cloud9* menu item.

<p align="center">
    <img alt="cloud9_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/cloud9_1.png" width="25%">
</p>

Click on the *Create environment* button to start creating a new environment.

<p align="center">
    <img alt="cloud9_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/cloud9_2.png" width="55%">
</p>

Enter **MyCloud9Environment** in the *Name* field, and click on the *Next step* button to continue.

<p align="center">
    <img alt="cloud9_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/cloud9_3.png" width="85%">
</p>

Leave the rest as it is, and click on the *Next step* button to continue.

<p align="center">
    <img alt="cloud9_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/cloud9_4.png" width="85%">
</p>

Review the parameters and click on the *Create environment* button.

<p align="center">
    <img alt="cloud9_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/cloud9_5.png" width="85%">
</p>

After a brief setup process, you will be taken to your newly created AWS Cloud9 environment. 

<p align="center">
    <img alt="cloud9_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/cloud9_6.png" width="85%">
</p>

### Download and install dependencies

To get your Cloud9 environment ready to deploy the EKS cluster, you will need to download and install some additional command line tools, such as **eksctl**, **kubectl**, and **jq**.

#### Download and install jq.

```
sudo yum -y install jq
```

#### Download and install kubectl

Download the Amazon EKS-vended **kubectl** binary.

```
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.16.8/2020-04-16/bin/linux/amd64/kubectl
```

Apply execute permissions to the binary.

```
chmod +x ./kubectl
```

Move the binary to a folder in your **PATH**.

```
sudo mv kubectl /usr/local/bin
```

Test your recently installed version of **kubectl**.

```
kubectl version --short --client
```

#### Download and install eksctl

Download the eksctl command-line tool.

```
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
```

Move the binary to a folder in your **PATH**.

```
sudo mv /tmp/eksctl /usr/local/bin
```

Test your recently installed version of **eksctl**.

```
eksctl version
```

### Create and attach an IAM role to your Cloud9 instance.

Click on the following [deep link](https://console.aws.amazon.com/iam/home#/roles$new?step=review&commonUseCase=EC2%2BEC2&selectedUseCase=EC2&policies=arn:aws:iam::aws:policy%2FAdministratorAccess) to open the IAM console and create a new role with Administrator access for your instance.

Make sure that the *AWS service* and *EC2* options are selected, then click *Next* to view permissions.

<p align="center">
    <img alt="iam_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/iam_1.png" width="85%">
</p>

Make sure that **AdministratorAccess** is checked, then click *Next* to review.

<p align="center">
    <img alt="iam_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/iam_2.png" width="85%">
</p>

Skip the tags by clicking on the *Next: Review* button.

<p align="center">
    <img alt="iam_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/iam_3.png" width="85%">
</p>

Enter *eks-cicd-cloud9-admin* as the role name, and click *Create role*.

<p align="center">
    <img alt="iam_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/iam_4.png" width="85%">
</p>

### Assign the newly created IAM role to your Cloud9 instance.

Click on the following [deep link](https://console.aws.amazon.com/ec2/v2/home?#Instances:tag:Name=aws-cloud9-MyCloud9Environment*;sort=desc:launchTime) to open the EC2 console and find your Cloud9 instance.

Click on *Actions*, select *Instance Settings*, and click *Attach/Replace IAM Role*.

<p align="center">
    <img alt="ec2_role_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/ec2_role_1.png" width="85%">
</p>

From the *IAM role* dropdown, select the **eks-cicd-cloud9-admin** role, and click on *Apply*.

<p align="center">
    <img alt="ec2_role_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/ec2_role_2.png" width="85%">
</p>

### Configure Cloud9 to use the newly assigned role.

Click on the gear at the top right corner, then click on *AWS Settings*, and disable the *AWS managed temporary credentials* option.

<p align="center">
    <img alt="cloud9_credentials" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/cloud9_credentials.png" width="85%">
</p>

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

Make sure Cloud9 is using the **eks-cicd-cloud9-admin** role that we created.

```
INSTANCE_PROFILE_NAME=`basename $(aws ec2 describe-instances --filters Name=tag:Name,Values=aws-cloud9-${C9_PROJECT}-${C9_PID} | jq -r '.Reservations[0].Instances[0].IamInstanceProfile.Arn' | awk -F "/" "{print $2}")`
aws iam get-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME --query "InstanceProfile.Roles[0].RoleName" --output text
```

The output should be the name of the role, **eks-cicd-cloud9-admin**.

### Start the EKS cluster provisioning.

The next step is to create the EKS cluster where we will be deploying our application. We will name the cluster **eks-cicd-lab-cluster**.

```
eksctl create cluster --name eks-cicd-lab-cluster --version 1.16 --region eu-west-1 --full-ecr-access --fargate --alb-ingress-access
```

Cluster provisioning takes approximately between 10-15 minutes. In the meantime, it is recommended that you proceed with instructions below.

### Prepare your application for deployment.

#### Create an Amazon ECR repository.

First, create the Amazon ECR repository where we'll store our images. Take note of the repository URI, as you will need it later to configure the CI/CD pipeline.

```
aws ecr create-repository --repository-name=eks-cicd-lab-ecr-repo | jq -r .repository.repositoryUri
```

Then, create an AWS CodeCommit repository where we'll store the application code. Take note of the clone URL, as you will need it to push the patched application into your AWS CodeCommit repo.

```
aws codecommit create-repository --repository-name=eks-cicd-lab-git-repo | jq -r .repositoryMetadata.cloneUrlHttp
```

We'll use a stripped-down version of the 2048 game available on GitHub as our test application.

```
cd ~/environment && git clone --bare https://github.com/alexwhen/docker-2048.git
```

Create a clone of the 2048 repository and push it into the AWS CodeCommit repository.

```
cd docker-2048.git && git push --mirror https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/eks-cicd-lab-git-repo
```

Clone the Virtual Immersion Week repository to get the application patches

```
cd ~/environment && git clone https://github.com/aws-samples/virtual-immersion-week-labs.git
```

Clone the AWS CodeCommit code repository.

```
cd ~/environment && git clone https://git-codecommit.eu-west-1.amazonaws.com/v1/repos/eks-cicd-lab-git-repo
```

Copy the patched files from the Virtual Immersion Week lab directory 

```
AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq -r .Account)
cp -f virtual-immersion-week-labs/cicd-eks-fargate/2048-patches/* ~/environment/eks-cicd-lab-git-repo
sed -i "s/<ACCOUNT_ID>/${AWS_ACCOUNT_ID}/g" ~/environment/eks-cicd-lab-git-repo/2048-game-deployment.yaml
```

Now, the AWS CodeCommit repository contains all the files needed to configure the build pipeline. Commit the changes to the repository and push them.

```
cd ~/environment/eks-cicd-lab-git-repo && git add . && git commit -m "Patched files added." && git push
```

### Create the build pipeline.

#### Create the AWS odeBuild project.

Click the *Services* menu at the top left corner of your screen and enter **CodeBuild**, then click on the AWS CodeBuild link.

<p align="center">
    <img alt="codebuild_1" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_1.png" width="25%">
</p>

Click on the *Create build project* button on the left.

<p align="center">
    <img alt="codebuild_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_2.png" width="85%">
</p>

In the *Project configuration* section, name your project **eks-cicd-build-pipeline-project**, and scroll down to the next section.

<p align="center">
    <img alt="codebuild_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_3.png" width="85%">
</p>

In the *Source* section:

 * Select **AWS CodeCommit** from the *Source provider* dropdown.
 * Select **eks-cicd-lab-git-repo** from the *Repository* dropdown.
 * Select the **master** branch from the *Branch* dropdown.

Leave the rest as is and scroll down to the next section.

<p align="center">
    <img alt="codebuild_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_4.png" width="85%">
</p>

In the *Environment* section, select:

 * *Managed image* as the type of environment image to use.
 * Choose **Amazon Linux 2** from the *Operating system* dropdown.
 * Choose **Standard** from the *Runtime(s)* dropdown.
 * Choose **aws/codebuild/amazonlinux2-x86_64-standard:3.0** from the *Image* dropdown.
 * Choose **Always use the latest image for this runtime version** from the *Image version* dropdown.
 * Choose **Linux** from the *Environment type* dropdown.
 * Check the *Privileged* checkbox.
 * Make sure all values are as depicted in the below screenshot.

<p align="center">
    <img alt="codebuild_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_5.png" width="85%">
</p>

Expand the *Additional Configuration Section*, and make sure you select the 3 GB memory, 2 vCPUs compute environment. Then, create four environment variables as follows:

| Variable name     | Value |
|-------------------|-------|
| ECR_REPO          | 012345678901.dkr.ecr.eu-west-1.amazonaws.com/eks-cicd-lab-ecr-repo |
| IMAGE_NAME        | 2048-game |
| EKS_ROLE_ARN      | arn:aws:iam::012345678901:role/eks-cicd-lab-codebuild-kubectl-role |
| CLUSTER_NAME      | eks-cicd-lab-cluster |

Where **012345678901** is your account number.

<p align="center">
    <img alt="codebuild_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_6.PNG" width="85%">
</p>

Make sure the *Buildspec* section remains as is, as shown in the screenshot below.

<p align="center">
    <img alt="codebuild_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_7.PNG" width="85%">
</p>

Scroll down to the bottom and click on the *Create build project* button.

<p align="center">
    <img alt="codebuild_8" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codebuild_8.png" width="85%">
</p>

### Create the AWS CodePipeline pipeline.

On the right sidebar, click the *Pipeline* dropdown and click on *Pipelines*. Then, click on *Create pipeline*.

<p align="center">
    <img alt="codepipeline_2" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codepipeline_2.png" width="85%">
</p>

Name your pipeline **eks-cicd-lab-pipeline**, and click on *Next*.

<p align="center">
    <img alt="codepipeline_3" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codepipeline_3.png" width="85%">
</p>

From the *Source provider* dropdown, choose **AWS CodeCommit**, then choose the **eks-cicd-lab-git-repo** repository from the *Repository name* dropdown. Then, choose the **master** branch from the *Branch name* dropdown, and click on *Next*.

<p align="center">
    <img alt="codepipeline_4" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codepipeline_4.png" width="85%">
</p>

Choose **AWS CodeBuild** from the *Build provider* dropdown, make sure the region is set to **Europe (Ireland)**, and choose the **eks-cicd-build-pipeline-project** you just created from the *Project name* search box. Click on *Next*.

<p align="center">
    <img alt="codepipeline_5" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codepipeline_5.png" width="85%">
</p>

Click on *Skip deploy stage*.

<p align="center">
    <img alt="codepipeline_6" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codepipeline_6.png" width="85%">
</p>

When presented with the dialog, click on *Skip*.

<p align="center">
    <img alt="codepipeline_7" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codepipeline_7.png" width="85%">
</p>

Click on *Create pipeline* to start the provisioning of the pipeline.

<p align="center">
    <img alt="codepipeline_8" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/codepipeline_8.png" width="85%">
</p>

### Create the kubectl role.

The pipeline will need to impersonate a role that is given system:masters privileges in the cluster. We start by replacing a placeholder in the **kubectl-role.json** file with your current account number, and creating the role using the AWS CLI and the patched file. The file is in the *virtual-immersion-week-labs/cicd-eks-fargate* directory in your Cloud9 environment. The role will be named **eks-cicd-lab-codebuild-kubectl-role**.

```
AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq -r .Account)
aws iam create-role --role-name eks-cicd-lab-codebuild-kubectl-role --assume-role-policy-document "$(cat ~/environment/virtual-immersion-week-labs/cicd-eks-fargate/kubectl-role.json | sed s/\<ACCOUNT_ID\>/$AWS_ACCOUNT_ID/g)"
```

### Check whether the cluster has already been created.

Your cluster should have already been provisioned for you by now. It is time to check whether it is ready to be configured.

Test that your **kubectl** configuration is correct.

```
kubectl get svc
```

You should see something like this:

```
NAME             TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
svc/kubernetes   ClusterIP   10.100.0.1   <none>        443/TCP   1m
```

Verify that two nodes have been created.

```
kubectl get nodes
```

The output should be similar to this:
```
NAME                                                    STATUS   ROLES    AGE    VERSION
fargate-ip-192-168-145-249.eu-west-1.compute.internal   Ready    <none>   9m6s   v1.16.8-eks-e16311
fargate-ip-192-168-159-100.eu-west-1.compute.internal   Ready    <none>   9m9s   v1.16.8-eks-e16311
```

Get the VPC ID of the newly created cluster. You will need this value to configure the ALB Ingress Controller.

```
eksctl get cluster --region eu-west-1 --name eks-cicd-lab-cluster -o json | jq -r .[0].ResourcesVpcConfig.VpcId
```

Now, create an IAM OIDC provider

```
eksctl utils associate-iam-oidc-provider --cluster=eks-cicd-lab-cluster --approve
```

### Create Fargate profile for 2048-game

Launch the AWS Fargate profile provisioning, and continue in another Terminal window.

```
eksctl create fargateprofile --cluster eks-cicd-lab-cluster --region eu-west-1 --name cicd-lab-fargate-profile --namespace 2048-game
```

### Configure the ALB Ingress Provider

The rbac_role manifest gives appropriate permissions to the ALB ingress controller to communicate with the EKS cluster we created earlier.

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/rbac-role.yaml
```

```
cd ~/environment && wget https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/alb-ingress-controller.yaml
```

Open the **alb-ingress-controller.yaml** in a Cloud9 tab, and change the following lines to look like these:

```
            # Setting the ingress-class flag below ensures that only ingress resources with the
            # annotation kubernetes.io/ingress.class: "alb" are respected by the controller. You may
            # choose any class you'd like for this controller to respect.
            - --ingress-class=alb

            # REQUIRED
            # Name of your cluster. Used when naming resources created
            # by the ALB Ingress Controller, providing distinction between
            # clusters.
            - --cluster-name=eks-cicd-lab-cluster

            # AWS VPC ID this ingress controller will use to create AWS resources.
            # If unspecified, it will be discovered from ec2metadata.
            - --aws-vpc-id=vpc-0acf523383430c8a0

            # AWS region this ingress controller will operate in.
            # If unspecified, it will be discovered from ec2metadata.
            # List of regions: http://docs.aws.amazon.com/general/latest/gr/rande.html#vpc_region
            - --aws-region=eu-west-1
```

The *--aws-vpc-id* value should be set to the cluster VPC that you obtained earlier.

Create an IAM Policy for the ALB Ingress Controller, so that it is able to create AWS resources on its own. Take note of the 

```
POLICY_ARN=$(aws iam create-policy \
    --policy-name ALBIngressControllerIAMPolicy \
    --policy-document https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/v1.1.4/docs/examples/iam-policy.json \
    | jq -r .Policy.Arn) 
```

Create an IAM service account.

```
eksctl create iamserviceaccount \
       --cluster=eks-cicd-lab-cluster \
       --namespace=kube-system \
       --name=alb-ingress-controller \
       --attach-policy-arn=$POLICY_ARN \
       --override-existing-serviceaccounts \
       --approve
```

```
kubectl apply -f alb-ingress-controller.yaml
```

```
kubectl logs -n kube-system $(kubectl get po -n kube-system | egrep -o alb-ingress[a-zA-Z0-9-]+)
```

#### Add the kubectl role to the authorized AWS roles.

```
AWS_ACCOUNT_ID=$(aws sts get-caller-identity | jq -r .Account)
ROLE="    - rolearn: arn:aws:iam::$AWS_ACCOUNT_ID:role/eks-cicd-lab-codebuild-kubectl-role\n      username: eks-cicd-lab-codebuild-kubectl-role\n      groups:\n        - system:masters"
kubectl get -n kube-system configmap/aws-auth -o yaml | awk "/mapRoles: \|/{print;print \"$ROLE\";next}1" > /tmp/aws-auth-patch.yml
kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
```

#### Add an inline policy to allow AWS CodeBuild to push and pull images from our Amazon ECR repository.

```
aws iam put-role-policy \
    --role-name codebuild-eks-cicd-build-pipeline-project-service-role \
    --policy-name CodeBuildEcrPolicy \
    --policy-document "$(cat ~/environment/virtual-immersion-week-labs/cicd-eks-fargate/codebuild-ecr-policy.json | sed s/\<ACCOUNT_ID\>/$AWS_ACCOUNT_ID/g)"
```
#### Add an inline policy to allow AWS CodeBuild to manage the cluster using kubectl.

```
aws iam put-role-policy \
    --role-name codebuild-eks-cicd-build-pipeline-project-service-role \
    --policy-name CodeBuildEksPolicy \
    --policy-document "$(cat ~/environment/virtual-immersion-week-labs/cicd-eks-fargate/codebuild-eks-policy.json | sed s/\<ACCOUNT_ID\>/$AWS_ACCOUNT_ID/g)"
```

### Create the namespace and the service.

First, create the **2048-game** namespace in Kubernetes. Our application pods will be placed into that namespace.

```
kubectl apply -f ~/environment/virtual-immersion-week-labs/cicd-eks-fargate/2048-k8s/2048-game-namespace.yaml
```

Then, create a service for our application.

```
kubectl apply -f ~/environment/virtual-immersion-week-labs/cicd-eks-fargate/2048-k8s/2048-game-service.yaml
```

And create an ingress for our application, so that it can be reached from the outside through an ALB.

```
kubectl apply -f ~/environment/virtual-immersion-week-labs/cicd-eks-fargate/2048-k8s/2048-game-ingress.yaml
```

### Start the deployment pipeline.

Make a small change in the application (which is in *~/environment/eks-cicd-lab-git-repo/2048*), e.g.: in the index.html. Then, commit the changes:

```
cd ~/environment/eks-cicd-lab-git-repo && git add . && git commit -m "Change to trigger the pipeline." && git push
```

Wait until the build is complete (you can monitor that from the AWS CodePipeline console), and then check the state of the pods:

```
kubectl get pods -n 2048-game
```

The result should look like this:
```
NAME                               READY   STATUS             RESTARTS   AGE
2048-deployment-5895dc87c-5sxsw    0/1     Pending            0          21s
2048-deployment-5895dc87c-924mq    0/1     Pending            0          13s
2048-deployment-5895dc87c-958vz    1/1     Running            0          74s
2048-deployment-5895dc87c-rfrpq    1/1     Running            0          74s
2048-deployment-5895dc87c-zkgcn    1/1     Running            0          74s
```

If you do not wait until pods reach the **Running** status, your ALB will return an HTTP 503 error. If your pods take more than two to three minutes to run, you may have forgotten to create the Fargate profile for the **2048-game** namespace, or you may have mistyped the namespace.

Now, get the address of the ALB that sits in front of the application containers:

```
kubectl get ingress/2048-ingress -n 2048-game
```

It should look like this:

```
NAME           HOSTS   ADDRESS                                                                  PORTS   AGE
2048-ingress   *       example.eu-west-1.elb.amazonaws.com                                      80      125m
```

Copy the address (in this case, **example.eu-west-1.elb.amazonaws.com**) into a new browser tag, and load it. If everything went well, you should see a screen like the one below:

<p align="center">
    <img alt="2048" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/feature/cicd-eks-fargate-lab/cicd-eks-fargate/img/2048.png" width="25%">
</p>

In case you see this screen, you have successfully completed the lab. Congratulations!
