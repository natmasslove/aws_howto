
# Sample scripts to prepare and run EMR Serverless Jobs

### Create resources (IAM Role, EMR Serverless Application, S3 bucket)
```
aws cloudformation deploy --stack-name cf-emrsrvless-sample ^
  --template-file cloudformation/010_emr_serverless.yaml --capabilities CAPABILITY_NAMED_IAM
```

### start run & watch execution

```
python source/run_job.py
```




### Clean-up

```
aws s3 rb s3://emr-serverless-demo-<<your_account_id>> --force
```

```
aws cloudformation delete-stack --stack-name 
```