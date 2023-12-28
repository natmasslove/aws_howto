# Choosing between AWS Glue and EMR Serverless for your Big Data Workloads

## Introduction

AWS provides a wide range of serverless technologies to run Big Data processing.
Sometimes those services have similar goals and it's difficult to choose - which one suits your needs better.
One good example is AWS Glue Jobs and EMR Serverless.

In this article we:
1. Cover some functional differences and service integrational aspects which might affect your choice
2. Provide benchmark test results (representing on one of typical steps in incremental data workloads)
3. Discuss scenarios where one technology or another could prevail

Disclaimer: in this article we focus on Glue Jobs specifically, paying less attention to other Glue capabilities whose purpose is not
data processing specifically. Nevertheless, Data Catalog and Crawlers might be essential part of you Data Platform no matter which
processing technology would you choose (Glue Jobs or EMR Serverless): they integrate with both very well.

## Functional aspects

### Service Maturity

**AWS Glue** was made generally available in 2017 (6 years ago - quite a long journey to these days standard) and got several major version upgrades making the service faster, more user-friendly and adding some additional capabilities.

**EMR Serverless** became GA only in mid-2022, but I wouldn't call it worrysome, as it was built taking experience from classic EMR on EC2.

Both services have a very good documentation and, also, github repositories with samples where you can get loads of code examples and explore usage best practices: [aws-glue-samples](https://github.com/aws-samples/aws-glue-samples), [emr-serverless-samples](https://github.com/aws-samples/emr-serverless-samples)

### Compatibility: Big Data Technology Stack

**EMR Serverless**: you can run Spark (PySpark, Scala, JAVA, SparkR) and HIVE jobs (as of time of this writing. The list is likely to be expanded in future).  
**AWS Glue**: support Spark only (PySpark and Scala scripts).  
In Glue you can also run pure Python code cheaply (using just 0.0625 of standard workers capacity), but it's not a scope for this article.

**Version upgrades**: EMR Serverless tends to be closer to the latest available Spark version as they declare 60 days interval to adopt newly released Spark versions while AWS Glue gets upgrades not that often.  

Current versions (as of 2023-12-29):  
**EMR Serverless**: version 6.15.0 -> Apache Spark 3.4.1 [link](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/release-versions.html)
**AWS Glue**: AWS Glue 4.0 -> Spark 3.3.0 [link](https://docs.aws.amazon.com/glue/latest/dg/release-notes.html)

### Compatibility: Open-table formats

It is easy to use both **EMR Serverless** and **Glue** to work with Open table formats (Hudi, Iceberg, Delta Lake).

- In Glue you just provide job parameter (e.g. *"--datalake-formats":"iceberg"* and some minimal spark configuration)
- In EMR-Serverless - you provide spark configuration options such as *spark.jars=/usr/lib/hudi/hudi-spark-bundle.jar*
- Using Open Table format is very well documented for both services

### Compatibility: AWS eco-system integration 

Both services are tightly integrated with such **core AWS services** as IAM, VPC, CloudFormation etc.
The same can be said for services typically used in data pipelines: S3 (not only for data, but for logs also), Data Catalog/Crawlers and many others.
Specifically 

Database and orchestration tools integration we'll discuss a bit later.

**AWS Glue Data Catalog**, even though it's a part of AWS Glue service, integrates with EMR just as easy.  
Providing this option for EMR serverless job run is sufficient (and it's a part of defaults as well):
```json
    "sparkSubmitParameters": {
        "spark.hadoop.hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
    }
```

### Job Scheduling and orchestration

1. Apache Airflow

Airflow provides easy-to-use operators for both Glue and EMR Serverless Jobs.
That's how running the job looks for EMR:
```python
from airflow.providers.amazon.aws.operators.emr import EmrServerlessStartJobOperator

    job_operator = EmrServerlessStartJobOperator(
        task_id="you_task_id",
        application_id=EMR_SERVERLESS_APPLICATION_ID,
        execution_role_arn=JOB_ROLE_ARN,
        job_driver={
            "sparkSubmit": {
                "entryPoint": f"s3://{S3_BASE_BUCKET}/scripts/your_script.py",
                "entryPointArguments": [S3_BASE_BUCKET]
            }
        }
    )
```

There are some additional operator when, for example in less common scenarios, you can create and tear-down the whole EMR Serverless application as well as running several jobs in between.

Both are equally well-integrated with Apache Airflow.

2. Step Functions

AWS-native orchestration service integrates with services in our scope very well and the implementation is done in similar way.

Defining State Machine task for Glue Job Run:
```json
"GlueJobRun": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "my-glue-job"
      }
      ...
    },
```

You can run asynchronously or wait for job completion using ".sync".

3. There's a native orchestration mechanism for Glue - Glue Workflows. Of course, it seamlessly integrates with Glue and not
available for EMR Serverless.
But as this option is less advanced than Airflow or Step Function, we wouldn't consider having it as a big advantage for Glue.

### Integration: Databases and data providers

1. AWS Databases: Redshift, RDS, Aurora

Typical approach in **EMR Serverless** (as well as in just plain PySpark) would be using JDBC:
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = (
    spark.read.format("jdbc")
    .option(
        "url", "jdbc:postgresql://<host_name>:<port>/<db_name>"
    )
    .option("driver", "org.postgresql.Driver")
    .option("user", "<username>")
    .option("password", "<password>")
    .load()
)
```
And, of course, you will need to retrieve DB credentials first (most likely from Secrets Manager).

In **AWS Glue** you can use built-in mechanism of Glue Connections, where you define connection properties alongside with
credentials (best practice is to reference pre-created secret). Then you can just like this:

```python
dynamic_frame_read = glueContext.create_dynamic_frame.from_options(
    connection_type="postgresql",
    connection_options={
        "connectionName": connection_name
        "dbtable": table_name,
        ...        
    }
)
```

This, in our opinion, makes it easier to implement database integrations in AWS Glue Jobs.

2. Other common data stores

In your data platform ... may need to .. SAP HANA, Snowflake

Glue .. provides out-of-the-box ... 
  same way - create connection
  list is growing

Saves your from hassle of picking correct JDBC driver, downloading it and integrating it into your job and, then, maintaining driver version etc. Which would be exactly EMR Serverless scenario for majority of data stores.




## Observability

- In Glue - very good + latest additions
    - Spark UI <<todo add screenshot>>
    - Observability metrics <<todo add screenshot>>
- In EMR - <<todo check>>

## Performance

### NYC Taxi ride test
- Test NYC Taxi convert
- Test NYC Taxi filter
  with 4 workers in Glue
  and 16vCPU in EMR Serverless
  <<todo run these tests>>

### Start-up times

- There's <<todo: check>> provisioned capacity for EMR serverless. But in this case objectively it's no longer a Serverless Technology

## Cost



- For smaller workloads EMR Serverless might be cheaper as you can start from 1 vCPU for super-small workload
- Whereas in AWS Glue minimum number of workers is 2 (4 vCPU each) 

## Technology maturity

- EMR Serverless announced <<todo check>>
- Glue started back in <<todo check>>

- Both has a very good documentation



##  Features (?) <<todo rephrase>>

### Specific additions (?) <<todo rephrase>>

- Glue provides Dynamic Data Frame which <<todo describe>>
- Glue provides Job bookmarks




## Conclusion

<<todo>>
There are several scenarios when you can prefer using EMR serverless:
- You intend to use something apart from PySpark
- You are migrating existing Big Data codebase into serverless platform. So even you PySpark jobs require less changes (adding GlueContext; parsing parameters using awsglue.utils getResolvedOptions etc.)
- Your workload elements tend to be small (e.g. 1 job just processing several gigabytes of data per run), so you can allocate less capacity
- Scenario: close to "lift-and-shift" migration scenario from EMR or Hadoop cluster

btw, if you are planning migration from existing EMR to EMR serverless, you might want to consider using EMR serverless cost estimator. [https://aws.amazon.com/blogs/big-data/amazon-emr-serverless-cost-estimator/]