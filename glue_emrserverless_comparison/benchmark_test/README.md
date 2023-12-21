

1. Deploy all resources:

```
aws cloudformation deploy --stack-name cf-glue-vs-emr-serverless --template-file cloudformation/010_resources.yaml --capabilities CAPABILITY_NAMED_IAM
```

2. Copy NYC rides dataset into our bucket (it works for us-east-1 region)
```
export s3_bucket_name="s3-glue-vs-emr-serverless-$(aws sts get-caller-identity --query 'Account' --output text)"
aws s3 cp s3://nyc-tlc/opendata_repo/opendata_webconvert/yellow/ s3://${s3_bucket_name}/nyc_rides_2022_csv/ --recursive
```