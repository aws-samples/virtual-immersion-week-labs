# Redshift lab

### Objective

The objective of this lab is to give you hands-on experience with AWS' fully-managed data warehouse service, [Amazon Redshift](https://aws.amazon.com/redshift/), as well as with Amazon Redshift Spectrum, a feature that lets you query external data.

<p align="center">
    <img alt="lab_architecture" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/lab_architecture.png" width="85%">
</p>

In this example we are going to create a Redshift cluster from scratch, populate it with data and run queries on it. Then, we are going to create an external schema and table, and use Redshift Spectrum to demonstrate how you can join data residing both in Redshift and in S3.

### A. Initialize your environment.

It is assumed that you have already created a Cloud9 environment in the previous lab. If not, you will be instructed on how to do so.

#### 1. Within the Cloud9 instance that you have created in the previous lab, run the following command in the terminal to clone this repository.
```
git clone https://github.com/aws-samples/virtual-immersion-week-labs.git && cd virtual-immersion-week-labs/redshift
```

#### 2. Run the initialization script to automatically create an S3 bucket and populate it.
```
bash initialize.sh
```
Write down the account ID that the script prints to the terminal. _This is important and will be used in a later step._

![account_id](https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/account_id.png "Account ID shown in terminal")

### B. Spin up and configure your Redshift cluster.

#### 1. Create the cluster

Click on the _Services_ menu in the console, and type in _Redshift_ in the search bar, or click on _Amazon Redshift_ under _Database_.

<p align="center">
    <img alt="menu_redshift" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/menu_redshift.png" width="85%">
</p>

Once on the Redshift console, click on the _Create cluster_ at the right of the screen.

<p align="center">
    <img alt="redshift_console" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/redshift_console.png" width="75%">
</p>

This will take you to the **Create cluster** console:
  * In the _Cluster configuration_ panel, enter **example-cluster** as your cluster identifier.
  * Right below, choose the **DC2.large** node type.
  * As for the number of nodes, we will be using the default value of **2**.
  
<p align="center">
    <img alt="cluster_config" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/cluster_configuration.png" width="75%">
</p>

Now you will configure database-specific parameters. Scroll down to the _Database configurations_ panel:
  * Leave **dev** as the database name and **5439** as the database port.
  * In the _Master user name_ field, leave **awsuser**.
  * Now choose a password and enter it in the _Master user password_ field. Recommended for this demo is: Redshift123

<p align="center">
    <img alt="database_config" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/database_configuration.png" width="75%">
</p>

As the final step before launching the cluster, scroll down to the _Cluster permissions_ panel and unfold it.
From the _Available IAM roles_, choose **Cloud9-myRedShiftRole** and click on the _Add IAM role_ button right of it.

<p align="center">
    <img alt="cluster_permissions" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/cluster_permissions.png" width="75%">
</p>

Now you are ready to launch the cluster. Scroll to the bottom of the page and click on _Create cluster_.

<p align="center">
    <img alt="create_cluster" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/create_cluster.png" width="85%">
</p>

#### 2. Create a connection to your cluster and open the query editor.

 * In the Redshift console, click on the _Editor_ icon on the left.
 * In order to use the editor, you need to create a connection to your cluster first.
   * In the _Connect to database_ panel, make sure the **example-cluster** cluster is selected from the _Cluster_ dropdown.
   * In the _Database name_ field, enter **dev**.
   * In the _Database user_ field, enter **awsuser**.
   * In the _Database password_ field, enter the password assigned to the **awsuser** user in the previous step.
   * Click on _Connect to database_.

<p align="center">
    <img alt="connect_to_db" src="https://github.com/aws-samples/virtual-immersion-week-labs/raw/master/redshift/img/connect_to_database.png" width="85%">
</p>

#### 3. Create the tables in Redshift.

Now you will create the tables contained by your Redshift instance. Copy and execute each of the CREATE TABLE statements individually in the query window. Make sure the query execution succeeds for every one of them.

```sql
CREATE TABLE users(
	userid integer not null distkey sortkey,
	username char(8),
	firstname varchar(30),
	lastname varchar(30),
	city varchar(30),
	state char(2),
	email varchar(100),
	phone char(14),
	likesports boolean,
	liketheatre boolean,
	likeconcerts boolean,
	likejazz boolean,
	likeclassical boolean,
	likeopera boolean,
	likerock boolean,
	likevegas boolean,
	likebroadway boolean,
	likemusicals boolean);
 
CREATE TABLE venue(
	venueid smallint not null distkey sortkey,
	venuename varchar(100),
	venuecity varchar(30),
	venuestate char(2),
	venueseats integer);

CREATE TABLE category(
	catid smallint not null distkey sortkey,
	catgroup varchar(10),
	catname varchar(10),
	catdesc varchar(50));

CREATE TABLE date(
	dateid smallint not null distkey sortkey,
	caldate date not null,
	day character(3) not null,
	week smallint not null,
	month character(5) not null,
	qtr character(5) not null,
	year smallint not null,
	holiday boolean default('N'));

CREATE TABLE event(
	eventid integer not null distkey,
	venueid smallint not null,
	catid smallint not null,
	dateid smallint not null sortkey,
	eventname varchar(200),
	starttime timestamp);

CREATE TABLE listing(
	listid integer not null distkey,
	sellerid integer not null,
	eventid integer not null,
	dateid smallint not null  sortkey,
	numtickets smallint not null,
	priceperticket decimal(8,2),
	totalprice decimal(8,2),
	listtime timestamp);

CREATE TABLE sales(
	salesid integer not null,
	listid integer not null distkey,
	sellerid integer not null,
	buyerid integer not null,
	eventid integer not null,
	dateid smallint not null sortkey,
	qtysold smallint not null,
	pricepaid decimal(8,2),
	commission decimal(8,2),
	saletime timestamp);
```

#### 4. Populate the tables.

Once the tables have been created, you can start populating them. During the initialization steps, a series of data files have been uploaded to an S3 bucket in your account. The name of the bucket is **redshift-demo-(ACCOUNT-ID)**, where **(ACCOUNT-ID)** is your account ID, which you obtained in step A.2.

You will use the Redshift COPY statement to do a bulk insertion of data from the S3 files directly into each table. The COPY statement takes in this case:
 * The URL to the S3 file that contains
 * The role that grants Redshift access to the S3 bucket that contains the data.
 * A delimiter, which separates the fields in the data file.
 * The region where the bucket resides.
 * Where necessary, the format of the datetime fields.

The statements that you need to run, are:

```sql
copy users from 's3://redshift-demo-012345678901/tickit/allusers_pipe.txt' 
credentials 'aws_iam_role=arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole' 
delimiter '|' region 'eu-west-1';

copy venue from 's3://redshift-demo-012345678901/tickit/venue_pipe.txt' 
credentials 'aws_iam_role=arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole' 
delimiter '|' region 'eu-west-1';

copy category from 's3://redshift-demo-012345678901/tickit/category_pipe.txt' 
credentials 'aws_iam_role=arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole' 
delimiter '|' region 'eu-west-1';

copy date from 's3://redshift-demo-012345678901/tickit/date2008_pipe.txt' 
credentials 'aws_iam_role=arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole' 
delimiter '|' region 'eu-west-1';
                            
copy event from 's3://redshift-demo-012345678901/tickit/allevents_pipe.txt' 
credentials 'aws_iam_role=arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole' 
delimiter '|' timeformat 'YYYY-MM-DD HH:MI:SS' region 'eu-west-1';

copy listing from 's3://redshift-demo-012345678901/tickit/listings_pipe.txt' 
credentials 'aws_iam_role=arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole' 
delimiter '|' region 'eu-west-1';

copy sales from 's3://redshift-demo-012345678901/tickit/sales_tab.txt'
credentials 'aws_iam_role=arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole' 
delimiter '\t' timeformat 'MM/DD/YYYY HH:MI:SS' region 'eu-west-1';
```

Where __012345678901__ is the account ID that you obtained in step A.2. _Remember to copy and run each of them individually._

#### 5. Query the data in Redshift

Now that you have loaded some data into your tables, you can begin testing. Here are some queries that you can use to test.

```sql
-- Get definition for the sales table.
SELECT *    
FROM pg_table_def    
WHERE tablename = 'sales';    

-- Find total sales on a given calendar date.
SELECT sum(qtysold) 
FROM   sales, date 
WHERE  sales.dateid = date.dateid 
AND    caldate = '2008-01-05';

-- Find top 10 buyers by quantity.
SELECT firstname, lastname, total_quantity 
FROM   (SELECT buyerid, sum(qtysold) total_quantity
        FROM  sales
        GROUP BY buyerid
        ORDER BY total_quantity desc limit 10) Q, users
WHERE Q.buyerid = userid
ORDER BY Q.total_quantity desc;

-- Find events in the 99.9 percentile in terms of all time gross sales.
SELECT eventname, total_price 
FROM  (SELECT eventid, total_price, ntile(1000) over(order by total_price desc) as percentile 
       FROM (SELECT eventid, sum(pricepaid) total_price
             FROM   sales
             GROUP BY eventid)) Q, event E
       WHERE Q.eventid = E.eventid
       AND percentile = 1
ORDER BY total_price desc;
```

### C. Create an external schema and table, and test Redshift Spectrum.

It is time now to test how Spectrum can be used to query data that lives in S3, and how data in Redshift can be joined with data in S3.

#### 1. Create an external schema and table.

In order to be able to query data in S3, you need to create a schema for tables that point to data outside Redshift. We will call our schema **spectrum**.

To create the **spectrum** schema, run the following SQL query:

```sql
create external schema spectrum 
from data catalog 
database 'spectrumdb' 
iam_role 'arn:aws:iam::012345678901:role/Cloud9-myRedshiftRole'
create external database if not exists;
```

Where __012345678901__ is the account ID that you obtained in step A.2. _Remember to copy and run each of them individually._

Now, let's create a table called **sales** within the **spectrum** schema, and have that table point to the _spectrum/sales_ prefix in S3. The initialization script has put some data there for you to query.

```sql
create external table spectrum.sales(
salesid integer,
listid integer,
sellerid integer,
buyerid integer,
eventid integer,
dateid smallint,
qtysold smallint,
pricepaid decimal(8,2),
commission decimal(8,2),
saletime timestamp)
row format delimited
fields terminated by '\t'
stored as textfile
location 's3://redshift-demo-012345678901/tickit/spectrum/sales/'
table properties ('numRows'='172000');
```

Where __012345678901__ is the account ID that you obtained in step A.2. _Remember to copy and run each of them individually._

By now, you have the **spectrum.sales** table pointing to your S3 bucket.

#### 2. Query data by joining tables in Redshift and S3.

At this point, you should be able to query data from both your data warehouse (Redshift) and your data lake (S3). Try running the following query:

```sql
SELECT TOP 10 spectrum.sales.eventid, SUM(spectrum.sales.pricepaid)
FROM spectrum.sales, event
WHERE spectrum.sales.eventid = event.eventid
AND spectrum.sales.pricepaid > 30
GROUP BY spectrum.sales.eventid
ORDER BY 2 DESC;
```

If you want to see what happens behind the scenes, you can add _EXPLAIN_ before the _SELECT_ statement to obtain the explain plan for the query.

```sql
EXPLAIN
SELECT TOP 10 spectrum.sales.eventid, SUM(spectrum.sales.pricepaid)
FROM spectrum.sales, event
WHERE spectrum.sales.eventid = event.eventid
AND spectrum.sales.pricepaid > 30
GROUP BY spectrum.sales.eventid
ORDER BY 2 DESC;
```
