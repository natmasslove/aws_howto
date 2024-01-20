
This folder contains scripts which can help you to measure Glue Job executions.
It runs the glue jobs, waits for the completion (measuring also how much time was spent in a particular state)
and, of course, logs everything :)

### Create a sample glue job (also auxiliary components: IAM Role, S3_bucket)

Create Cloudformation Stack containing essiential resources:

```
aws cloudformation deploy --stack-name cf-glue-runner-sample --template-file cloudformation/010_resources.yaml --capabilities CAPABILITY_NAMED_IAM
```



### Execute the Glue Job and collect information

```
python source/glue_job_run.py
```

### Clean-Up

Clean-up S3 bucket before stack deletion.
```
aws s3 rb s3://s3-glue-runner-sample-<<your_account_id>> --force
```

```
aws cloudformation delete-stack --stack-name cf-glue-runner-sample
```