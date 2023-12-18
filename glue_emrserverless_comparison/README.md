# Choosing between AWS Glue and EMR Serverless for your Big Data Workloads

## Introduction

<<todo>>
AWS provides a wide set of serverless technologies.
Glue & EMR - for big data processing (specifically EMR serverless, as we are talking serverless)


## Compatibility

### Big Data Technology Stack

- In EMR Serverless you can run both Spark and HIVE job
- In EMR Serverless: Spark written in pySpark, Scala, ...
<<todo - check>>
- In Glue - PySpark only
<<todo - check>>
- In Glue you can run pure Python code cheaply (using 0.0625 workers capacity), but it's not a scope for this article

### Open-table format

How it is easy to use Open table formats (Hudi, Iceberg, Delta Lake) with the technology.

- In Glue you just provide job parameter (e.g. "--datalake-formats":"iceberg" and some minimal spark config)
- In EMR <<todo - check>>
https://www.youtube.com/watch?v=CIsdaooeVw4

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