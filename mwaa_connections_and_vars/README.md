
# How to setup and use connections and variables in AWS managed Apache Airflow

Amazon Managed Workflows for Apache Airflow (MWAA) provides a very nice and easy way to manage Airflow Cluster.
It's not only about spinning up or maintaining the cluster, but the integration with other AWS Services as well.

Specifically, it's AWS Secrets Manager which can be used to store Airflow Connections and Variables.
This gives us the following benefits:
- Connection details are stored in centralized secure place
- Connections can be used by multiple Airflow clusters or even other services while still maintained in one place
- A separate security or operation team can maintain or update connection details (host change, password rotation etc.) without need to log into Airflow cluster

In this guide we provide step-by-step instructions on how to set up and use secrets manager-based connections and variables.
It also includes cloudformation templates and sample DAG code, so you can easily integrate this solution into your project.

Full source code is stored in Git Repository: https://github.com/natmasslove/aws_howto/tree/main/mwaa_connections_and_vars

## Secrets manager-based Connections: How it works

<<todo:>>
Add diagrams


## Settings in your Airflow cluster to work with Secrets Manager and connect to DB

In this section we walk you through the process of creating (or modifying) Airflow cluster.
Apart from usual, there are additional requirements for our use-case are:
1. *IAM Role* associated with you Airflow cluster should have permissions to access secrets
2. Python Libraries to interact with database should be installed (via *requirements.txt* file)

Steps to create and properly set up Airflow cluster:
1. Make sure your VPC is set up correctly to host Airflow cluster
   You can check the networking requirements with AWS documentation here: https://docs.aws.amazon.com/mwaa/latest/userguide/networking-about.html
   Alternatively, you can create a new VPC using a cloudformation template from git source code: cloudformation\010_vpc.yaml:
```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-010-vpc"

  aws cloudformation deploy \
    --template-file cloudformation/010_vpc.yaml \
    --stack-name $stack_name \
    --no-fail-on-empty-changeset \
    --parameter-overrides ProjectName=$project_name
```
*Note: we use project_name value as a part of the name of each resource in this demo.*

2. Create S3 bucket for Airflow Cluster and upload sample DAGs and requirements.txt files there

2.1 S3 creation via CloudFormation Stack:
```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-015-s3"

  aws cloudformation deploy \
    --template-file ../cloudformation/015_s3.yaml \
    --stack-name $stack_name \
    --no-fail-on-empty-changeset \
    --parameter-overrides ProjectName=$project_name
```    

2.2 Deploy DAGs and requirements.txt
*Note: script determines s3 bucket name dynamically. If you changed the bucket name in previous step - please make changes to the following script accordingly*
```bash
  export project_name="mwaa-secrets-demo"
  account_id=$(aws sts get-caller-identity --query "Account" --output text | tr -d '\r')
  s3_bucket_name="s3-${project_name}-${account_id}"  

  aws s3 sync ../airflow s3://${s3_bucket_name}/ --delete
```   

3. Create Managed Airflow cluster and its IAM Role

Notes:
- Airflow cluster requires 


```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-020-mwaa"

  aws cloudformation deploy \
    --template-file ../cloudformation/020_mwaa.yaml \
    --stack-name $stack_name \
    --no-fail-on-empty-changeset \
    --parameter-overrides ProjectName=${project_name} MWAAS3Bucket=$s3_bucket_name MWAASecurityGroupIds=$security_group_id MWAASubnetIds=$private_subnets_csv \
    --capabilities CAPABILITY_NAMED_IAM
```   





## Considerations when using Connections and Variables in Secrets Manager

<<todo:>> - pricing

## Clean Up

<<todo:>>