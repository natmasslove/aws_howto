# Sample scripts to prepare and run EMR Serverless Jobs

Some useful scripts demonstrating how we can interact with AWS EMR Serverless.

1. "cloudformation" folder - contains a template which creates: EMR Serverless Application, IAM Role for Serverless Job and some auxiliary resources
2. "spark_scripts" folder - contains one sample (and simple :) ) job to convert s3-based csv into parquet
3. "source" folder - contains helpers lib to interact with EMR serverless (start job run, wait for it's completion and gather execution stats) and sample script which uses the lib.

Here’s what you’ll find in this hands-on example:
* cloudformation: This section includes a CloudFormation template. It's designed to set up your EMR Serverless Application and an IAM Role for Serverless Jobs, along with a few additional resources.
* spark_scripts: Contains one sample (and simple :) ) job to convert s3-based csv into parquet.
* source: Contains a library of helper scripts that facilitate interaction with EMR Serverless (start job run, wait for it's completion and gather execution stats) and a sample script which uses the lib.

### Create resources (IAM Role, EMR Serverless Application, S3 bucket)
```
aws cloudformation deploy --stack-name cf-emrsrvless-demo ^
  --template-file cloudformation/010_emr_serverless.yaml --capabilities CAPABILITY_NAMED_IAM
```

### Start run & Watch execution
```
python source/run_job.py
```

### Clean-up

Clean-up S3 bucket before stack deletion.
```
aws s3 rb s3://s3-emr-serverless-demo-<<your_account_id>> --force
```

```
aws cloudformation delete-stack --stack-name cf-emrsrvless-demo
```