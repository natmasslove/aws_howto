# How to accelerate your Glue Job development with Glue Interactive Sessions

In Glue Job development debugging part might become especially cumbersome.  
Each time you run Glue Job you have to wait up to several minutes for Job startup and, sometimes, just get an error message for
incorrect syntax or something else really simple.

There are several ways to speed up the process by partially developing code locally (for example using Docker container tailored for Glue).
In this article we will focus on another approach - using Glue interactive sessions, as it seems to be the fastest to configure and
very close to mimic environment and permissions you get during Glue Job execution.

We will go through the following steps:
1. Set Up (configuration should be done just once):
  - IAM Role for Interactive Sessions (or preferably re-use an IAM Role you intend to use with your Glue Jobs)
  - install Jupyter (if you don't have this installed locally)
  - installing required libraries and setting up AWS CLI profile
2. Debugging your Spark code inside Jupyter Notebook which can mimic step-by-step Glue Job execution
3. Converting your Jupyter Notebook into Glue Job script

Note: Using Interactive sessions are billed based on DPU you use (which correlates to number of workers). Minimum is 2 workers, so based on current pricing it's $0.80/hour. This might be considered as aprooach's downside, but it is outweighted, in our opinion, by the development acceleration.

## Setting Up Interactive Sessions

1. Let's create Python virtual environment and install required libraries:
```shell
python -m venv jupyterenv
call jupyterenv/scripts/activate

pip3 install --upgrade jupyter boto3 aws-glue-sessions

install-glue-kernels
```

2. Here we create an IAM role which will be used by Jupyter Notebook to run commands:
```shell
aws cloudformation deploy --template-file cloudformation/gluerole.yaml --stack-name cf-glueintsessiondemo-role --capabilities CAPABILITY_NAMED_IAM
```

Please note the ARN of IAM Role in CloudFormation stack's outputs. We will use it in Jupyter session initialization.

This IAM Role contains:
- Managed Service policies for Glue Interactive Sessions
- You can add your own policies here. For example, if you you need to read/write S3 objects - it would required additional policy attached to the role. Solely for demo purposes we use AmazonS3FullAccess policy here instead of fine-grained one.

3. Configure you AWS credentials

In aws credentials (<HOME_DIR>/.aws/credentials) you need to create (or re-use existing) profile.
The easiest way to give user sufficient privileges are:
- add AWSGlueConsoleFullAccess managed policy
- add policy allowing iam:PassRole on a role created before

That's how it could look like (replace with your values)
```ini
[profile_for_article]
region=<put your region here>
aws_access_key_id=<put your access key here>
aws_secret_access_key=<put your secret access key here>
```
We will use profile named "profile_for_article" from now on.

<<todo>>

## Starting your Jupyter Notebook and debugging the code
 
1. Let's start a new Jupyter Notebook:

- Run command
```shell
jupyter notebook
```
- Click New -> Notebook
- Choose "Glue PySpark" as the Kernel

2. In the notebook let's do some initialization:

(replace with your values)
```
%profile profile_for_article
%iam_role <put your IAM role here>
%idle_timeout 10
%number_of_workers 2
```

%idle_timeout - The number of minutes of inactivity after which session is stopped. A nice feature not to bloat your AWS bill.
%number_of_workers - you can choose required number of workers (while 2 is minimum). It depends on the processing power you need. Here we
keep it as small as possible for demo purposes.

3. Now let's start our session:
```python
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
```
This code is identical to what we have in the beginning of our typical Glue Job.
It will take some time (around 30-40 second) to get ready and we can start developing our code!

Note: The moment after session creation is when he billing starts.

4. Now let's do some coding. We want to develop a simple flow which 
- reads CSV data from S3 (we'll use a sample csv file containing data about 50 lakes on Earth)
- converts it into Parquet and saves it to S3's output folder
- aggregates data and shows number of lakes per continent in this dataset

Upload sample data onto S3:
- create S3 bucket (we use "s3-glueintsessionsdemo-data" in this article, while you'll need to come up with your own name)
- upload lakes.csv file (from "sample_data" git folder) into "in/lakes/"

5. Let' add some cells into our notebook:

**Reading data** (don't forget s3_bucket_name value with your bucket):
```python
# Declaring the S3 bucket name variable
s3_bucket_name = "s3-glueintsessionsdemo-data"

# 1. Read dataframe directly from s3 object using the variable
df = spark.read.option("header", "true").option("inferSchema", "true").csv(f"s3://{s3_bucket_name}/in/lakes/")
```

**Writing in Parquet format**:
```python
# 2. Convert it into parquet format and writes to specified S3 path using the variable
df.write.mode("overwrite").parquet(f"s3://{s3_bucket_name}/out/lakes/")
```

**Aggregate and output**:
```python
# 3. Prepare aggregated dataframe
agg_df = df.groupBy("continent").count().withColumnRenamed("count", "number_of_lakes")

# Write aggregated dataframe to another S3 path using the variable
agg_df.write.mode("overwrite").parquet(f"s3://{s3_bucket_name}/out/lakes/aggregated/")

# Outputs dataframe
agg_df.show()
```

**Stopping Interactive session**:
```python
%stop_session
```

## Converting the Notebook into Glue Job script

<<todo>>


## Clean Up

<<todo>>
1. empty S3 bucket and delete it
2. delete cloudformation template