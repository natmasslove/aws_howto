# Choosing between AWS Glue and EMR Serverless for your Big Data Workloads

## Introduction

<<todo>>
AWS provides a wide set of serverless technologies.
Glue & EMR - for big data processing (specifically EMR serverless, as we are talking serverless)

<<This article's intent is to provide your information for choosing between ....

<<First we cover some functionality aspects which might affect your choice
<<Then, we provide the results of benchmark test we conducted to assess their cost and performance 



## Compatibility

### Big Data Technology Stack

- In EMR Serverless you can run both Spark and HIVE job
- In EMR Serverless: Spark written in pySpark, Scala, ...
<<todo - check>>
- In Glue - Spark (Python and Scala)
<<todo - check>>
- In Glue you can run pure Python code cheaply (using 0.0625 workers capacity), but it's not a scope for this article

### Open-table format

It is easy to setup both EMR Serverless and Glue to work with Open table formats (Hudi, Iceberg, Delta Lake).

- In Glue you just provide job parameter (e.g. "--datalake-formats":"iceberg" and some minimal spark config)
- In EMR provide spark configs such as
spark.jars=/usr/lib/hudi/hudi-spark-bundle.jar
- Using Open Table format is very well documented for both services


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

- Versions:
  EMR Serverless is updated more often to catch up with latest Spark versions.
  For example:
  Glue : AWS Glue 4.0 -> Spark 3.3.0,  https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
  EMR Serverless: 6.15.0 -> Apache Spark	3.4.1
  https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/release-versions.html

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

btw, if you are planning migration from existing EMR to EMR serverless, you might want to consider using EMR serverless cost estimator. [https://aws.amazon.com/blogs/big-data/amazon-emr-serverless-cost-estimator/]