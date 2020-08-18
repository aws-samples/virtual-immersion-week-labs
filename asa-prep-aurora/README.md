
# LAB 03 Launch a new Aurora Database Cluster

## 0. Before your start

- 0.1. Login to the **AWS Console**
- 0.2. Make sure you are in the `Ireland` region.

## 1. Create a new Security Group

- 1.1. Open the **VPC** service console
- 1.2. Click on `Security Groups` under the SECURITY sub menu
- 1.3. Modify the default security group selecting the check box next to it and clicking Actions ->  Edit inbound
- 1.4. Set the following options on the configuration screen for the new security group:
    - In the **Inbound rules** section:
        - Add a new rule. Set the type to `MySQL/Aurora`, source to `172.31.0.0/16` and description to `allow mysql traffic from the VPC`
    - Click `Save rules` to modify the default security group

## 2. Create the DB cluster

- 2.1. Open the **Amazon RDS** service console
- 2.2. Click `Create database` to start the configuration process
- 2.3. Set the following options on the configuration screen for the new DB cluster:
    - In the **Choose a database creation method** section:
        - Ensure the `Standard Create` option is selected.
    - In the **Engine options** section:
        - Choose the `Amazon Aurora` engine type
        - Choose the `Amazon Aurora with MySQL compatibility` edition
        - Select the `Aurora (MySQL)-5.6.10a` version
        - Select the `Regional` database option
    - In the **Database features** section:
        - Select the `One writer and multiple readers` option
    - In the **DTemplates**D section:
        - Select the `Production` option
    - In the **Settings** section:
        - Set the DB cluster identifier to `auroralab-mysql-cluster`
        - Set the Master username to `masteruser`. This is the user account with the most elevated permissions in the database
        - Do **not** check the `Auto generate a password` option
        - Set the Master password to `AsaPrep-Wave1-2020` and confirm the password
    - In the **DB instance** size section:
        - Select Memory Optimized classes, and choose `db.r5.large` in the size drop-down
    - In the **Availability & durability** section:
        - Choose `Create an Aurora Replica/Reader node` in a different AZ
    - In the **Connectivity** section:
        - Pick the default Virtual Private Cloud (VPC)
        - Expand the sub-section 'Additional connectivity configuration'
        - The DB subnet group will be selected automatically once you the VPC
        - Make sure the cluster Publicly accessible option is set to **No**.
        - At VPC security group, choose the `default` security group
    - Expand the **Additional configuration** section, and configure options as follows:
        - Set the Initial database name to `mylab`
        - Set Backup retention period to `1 day`
        - Check the box to `Enable encryption`
        - Set the Master key to `[default] aws/rds`.
        - Check the box to `Enable Backtrack`.
        - Set a Target backtrack window of `24` hours.
        - Check the box to `Enable Performance Insights`.
        - Set a Retention period of `Default (7 days)`.
        - Set the Master key to `[default] aws/rds`.
        - Check the `Enable Enhanced Monitoring` box.
        - Select a Granularity of `1 second`.
        - For Log exports check the `Error log` and `Slow query` log boxes.
        - De-select/turn off the check box `Enable delete protection`. In a production use case, you will want to leave that option checked, but for testing purposes, un-checking this option will make it easier to clean up the resources once you have completed the lab.
    - Click `Create database` to provision the DB cluster.


## 3. Retrieve the DB cluster endpoints

There are two endpoints created by default. The Cluster Endpoint will always point to the writer DB instance of the cluster, and should be used for both writes and reads. The Reader Endpoint will always resolve to one of the reader DB instances and should be used to offload read operations to read replicas. 

- 3.1 In the RDS console, go to the DB cluster detail view by clicking on the cluster DB identifier.
- 3.2 The Endpoints section in the Connectivity and security tab of the details page displays the endpoints. Note these values down, as you will use them later.

## 4 Verify DB cluster

- 4.1. Open the **Clolud9** service console
- 4.2. Click on `Create Environment`
    - In the **Environment name and description** section:
        - Choose a name for your instance `mylabInstance`
    - In the **Environment settings** section:
        - Environment type: `Create a new EC2 instance for environment (direct access)`
        - Instance type: `t2.micro (1 GiB RAM + 1 vCPU)`
        - Platform: `Amazon Linux`
    - Click on `Create environment` to create a new Cloud9 environment
- 4.3. Locate and expand terminal window located at the bottom of the screen
- 4.4. Connect to your instance by typing the following commands, one by one. Make sure you replace the `{clusterEndpoint}` place holder with the value of the cluster endpoint created in the preceding steps:
```
export DBUSER=masteruser
export DBPASS=AsaPrep-Wave1-2020
export ENDPOINT={clusterEndpoint}
mysql -h$ENDPOINT -u$DBUSER -p"$DBPASS" -e"SELECT @@aurora_version;"
```
Congratulations! You should receive a message like the one below. Confirming you have access to your new Aurora Instance.

```
TeamRole:~/environment $ mysql -h$ENDPOINT -u$DBUSER -p"$DBPASS" -e"SELECT @@aurora_version;"
+------------------+
| @@aurora_version |
+------------------+
| 1.17.8           |
+------------------+
```
