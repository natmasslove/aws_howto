
* [Introduction](#introduction)
* [General Steps to setup up Glue to work with JDBC sources](#general-steps)

# How to Connect AWS Glue to Snowflake and SAP HANA Databases

If you're looking to set up AWS Glue jobs and connections to work with Snowflake and SAP HANA databases, this article provides a step-by-step guide to help you get started. 

We also provide CloudFormation code for creating the necessary resources, as well as best practices for storing credentials in Secrets Manager rather than in the connection itself.

Described approach can be applied to other JDBC sources as well.

<a id="general-steps"></a>
## General Steps to setup up Glue to work with JDBC sources

Before you get started, make sure you have an S3 bucket to store your Glue job scripts and artifacts, such as JDBC drivers
(it can also be created using steps from Prerequisites section of this guide).

Then follow these general steps to set up Glue to work with JDBC sources:

1. Create a secret in Secrets Manager that stores your credentials.
2. Download the JDBC driver and upload it into your Glue S3 bucket.
3. Create a Glue connection:
    - Provide a JDBC string.
    - Reference the JDBC driver location on S3.
    - Reference the previously created secret.

To test the connectivity, follow these additional steps:

4. Create a Glue job (sample code is provided in the "glue" folder).
5. Run the Glue job to test the connectivity.

<a id="prerequisites"></a>
## Prerequisites

In this step we create a bucket where we place the sample glue job scripts and JDBC drivers.
```bash
aws cloudformation create-stack --stack-name cf-awshowto-glueconn-010-s3 \
    --template-body file://cloudformation/010_s3.yaml
```

By default, it creates bucket named "s3-awshowto-glueconn-${AWS::AccountId}-glue". You can change the name it by modifying cloudformation/010_s3.yaml.

<a id="download-glue-drivers"></a>
## Snowflake Connection


# How to store Glue Connection's credentials in Secrets Manager


# Implementation for 