
# Intro
**The problem**: I would like to use project helpers in my AWS Glue Job (Job type is Pythonshell).  

It would have been pretty straightforward for Glue Spark job: just zip you project_helpers folder, upload to S3 and
point to the file using '--extra-py-files' parameter.

For Pythonshell jobs this approach doesn't work. You need to create a python wheel package for you library.

These are sample steps to make it work.

# Steps
1. Create AWS Resources:
```bash
export s3_bucket_name=s3-wheeltest-amaslov #put your own bucket name here

export stack_name="cfrm-wheeltest"

aws cloudformation deploy --template-file cloudformation/010_resources.yaml \
  --stack-name $stack_name --no-fail-on-empty-changeset \
  --parameter-overrides ArtifactsBucketName=$s3_bucket_name --capabilities CAPABILITY_NAMED_IAM
```
**It creates:**
- S3 bucket (where we deploy glue job artifacts to)
- IAM Role for Glue Job (with minimal permissions)
- Glue Job (please note extra-py-files parameter)

```yaml
      DefaultArguments:
        "--extra-py-files": !Sub 's3://${ArtifactsBucketName}/glue/project_helpers-0.1-py3-none-any.whl'        
```

2. Create a wheel file
```bash
cd python # for me building a wheel package worked only from code folder
python setup.py bdist_wheel
cd ..
```

setup.py is responsible for creating "project_helpers" package with "calculator" module in it.


3. Deploy GlueJob script and Wheel package to S3

```bash
aws s3 cp python/glue_script.py s3://$s3_bucket_name/glue/

aws s3 cp python/dist/project_helpers-0.1-py3-none-any.whl s3://$s3_bucket_name/glue/
```

4. Now you can run Glue Job, so output will look like this:

```
2023-07-04T15:47:30.816+03:00	Installing collected packages: project-helpers
2023-07-04T15:47:30.863+03:00	Successfully installed project-helpers-0.1
2023-07-04T15:47:31.052+03:00	[notice] A new release of pip available: 22.1.2 -> 23.1.2 [notice] To update, run: pip install --upgrade pip
2023-07-04T15:47:31.180+03:00	Setup complete. Starting script execution: ----
2023-07-04T15:47:31.183+03:00	8 -2
```
Note that 8 and -2 are result of our small test 😃

# Clean Up
```bash
aws s3 rm s3://$s3_bucket_name --recursive  # so it won't fail while deleting via CloudFormation as S3 bucket is not empty

aws cloudformation delete-stack --stack-name $stack_name

```