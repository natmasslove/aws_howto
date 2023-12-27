# Choosing between AWS Glue and EMR Serverless for your Big Data Workloads

## Introduction

AWS provides a wide range of serverless technologies to run Big Data processing.
Sometimes those services have similar goals and it's difficult to choose - which one suits your needs better.
One good example is AWS Glue Jobs and EMR Serverless.

In this article we:
1. Cover some functionality differences which might affect your choice
2. Provide benchmark test results (representing on one of typical steps in incremental data workloads)
3. Discuss scenarios where one technology or another could prevail

Disclaimer: in this article we focus on Glue Jobs specifically, paying less attention to other Glue capabilities whose purpose is not
data processing specifically. Nevertheless, Data Catalog and Crawlers might be essential part of you Data Platform no matter which
processing technology would you choose (Glue Jobs or EMR Serverless): they integrate with both very well.

## Functional aspects

### Service Maturity

**AWS Glue** was made generally available in 2017 (6 years ago - quite a long journey to these days standard) and got several major version upgrades making the service faster, adding more capabilities and making the service more user-friendly.

**EMR Serverless** became GA only in mid-2022, but I wouldn't call it worrysome, as it was built taking experience from classic EMR on EC2.

Both services have a very good documentation and, also, github repositories with samples where you can get some example pieces of code and explore usage best practices: [aws-glue-samples](https://github.com/aws-samples/aws-glue-samples), [emr-serverless-samples](https://github.com/aws-samples/emr-serverless-samples)

### Compatibility: Big Data Technology Stack

**EMR Serverless**: you can run Spark (PySpark, Scala, JAVA, SparkR) and HIVE jobs (as of time of this writing. The list is likely to be expanded in future).  
**AWS Glue**: support Spark only (PySpark and Scala scripts).  
In Glue you can also run pure Python code cheaply (using 0.0625 standrard workers capacity), but it's not a scope for this article.

**Version upgrades**: EMR Serverless tends to be closer to the latest available Spark version as they declare 60 days interval to adopt newly released Spark versions while AWS Glue gets upgrades not that often.  

Current versions (as of 2023-12-29):  
**EMR Serverless**: version 6.15.0 -> Apache Spark 3.4.1 [link](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/release-versions.html)
**AWS Glue**: AWS Glue 4.0 -> Spark 3.3.0 [link](https://docs.aws.amazon.com/glue/latest/dg/release-notes.html)

### Compatibility: Open-table formats

It is easy to use both **EMR Serverless** and **Glue** to work with Open table formats (Hudi, Iceberg, Delta Lake).

- In Glue you just provide job parameter (e.g. *"--datalake-formats":"iceberg"* and some minimal spark configuration)
- In EMR-Serverless - you provide spark configuration options such as *spark.jars=/usr/lib/hudi/hudi-spark-bundle.jar*
- Using Open Table format is very well documented for both services

### AWS eco-system integration 

Glue Data Catalog




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

### Job Scheduling and orchestration

- Glue has it's own mechanism (using Glue Workflows and Glue trigger), which is not advanced, but for small workloads - ok.
- <<todo:>> check how they integrate with Step Functions
- <<todo:>> check how they integrate with Airflow
- <<todo:>> is there a EMR scheduled jobs


## Conclusion

<<todo>>
There are several scenarios when you can prefer using EMR serverless:
- You intend to use something apart from PySpark
- You are migrating existing Big Data codebase into serverless platform. So even you PySpark jobs require less changes (adding GlueContext; parsing parameters using awsglue.utils getResolvedOptions etc.)
- Your workload elements tend to be small (e.g. 1 job just processing several gigabytes of data per run), so you can allocate less capacity
- Scenario: close to "lift-and-shift" migration scenario from EMR or Hadoop cluster

btw, if you are planning migration from existing EMR to EMR serverless, you might want to consider using EMR serverless cost estimator. [https://aws.amazon.com/blogs/big-data/amazon-emr-serverless-cost-estimator/]