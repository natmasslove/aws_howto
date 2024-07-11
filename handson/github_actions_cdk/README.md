# Setting Up your GitHub action workflows to deploy AWS CDK projects

## Prerequisites and goals

There is a simple AWS CDK (Python) project which creates just one resource (SSM Parameter).

In order to go through this example you should:
- Have AWS account
- Be able to create IAM user in this account
- Have a github repo (you should be able to create secrets in this repo)

Goal:
- To create a pipeline which can deploy / destroy AWS CDK projects' resources

## Preparation

### IAM User
1. Create IAM user (let's call it github_service_user)
2. Add the following permissions for the user (the simplest is to create inline policy):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Resource": [
                "arn:aws:iam::*:role/cdk-*-deploy-role-*",
                "arn:aws:iam::*:role/cdk-*-file-publishing-role-*"
            ]
        }
    ]
}
```
These are minimal permission that worked.
3. Generate ACCESS_KEYs for the user (note those down)

### AWS Credentials in GitHub repo
1. In your GitHub repo browse to: Settings -> Secrets & variables.
2. Create to repository secrets:
   - Name "AWS_ACCESS_KEY_ID", put IAM user's AWS_ACCESS_KEY_ID value here
   - "AWS_SECRET_ACCESS_KEY" and IAM user's AWS_SECRET_ACCESS_KEY

### Create workflow
1. In your GitHub repo create a folder ".github/workflows".
2. Put .yml/.yaml file inside this folder.
3. Sample YAML file which prepares CDK environment and runs DEPLOY & DESTROY commands for the sample CDK project - github-actions-demo.yml in this folder. 


