
# Hand-on: Create, Test (locally) and Deploy container-based Lambda

This hands-on demonstrates how to host python code in container used by Lambda.

## 1. Create Lambda code and prepare Docker Image

Refer to the `app.py` and `Dockerfile` from "`src/`" folder as sample.

Navigate to `src/` and run the following commands:

This builds a docker image from app.py. Foundation image is the one provide by AWS in public repo (public.ecr.aws/lambda/python:3.13)

```bash
docker build -t lambda-container .
```

To check if image is created:

```bash
docker images
```

Run container locally:

```bash
docker run -p 9000:8080 lambda-container
```

Test the Lambda Function locally:

in LiNUX:

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"key": "value"}'
```

on Windows (double quotes matter):

```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d "{""key"": ""value""}"
```

## 2. Upload image and deploy lambda

1. Upload image into ECR (ECR repository should be created beforehand)

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin {account_id}.dkr.ecr.{region}.amazonaws.com

docker tag lambda-container:latest {account_id}.dkr.ecr.{region}.amazonaws.com/{repo/image}:latest

docker push {account_id}.dkr.ecr.{region}.amazonaws.com/{repo/image}:latest
```

2. Create Lambda Function and its IAM Role from terraform repo:

Navigate to `terraform` folder. Change your repo/image name

Run

```bash
terraform init

terraform apply -var="ecr_repo_name=my-custom-repo-name"
```