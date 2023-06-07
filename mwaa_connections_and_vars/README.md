
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

In this section we will walk you through the process of creating (or modifying) Airflow cluster.  
Apart from usual, there are additional requirements for our use-case are:
1. *IAM Role* associated with you Airflow cluster should have permissions to access secrets
2. Python Libraries to interact with database should be installed (via *requirements.txt* file)

Steps to create and properly set up Airflow cluster:
### 1. Make sure your VPC is set up correctly to host Airflow cluster
   You can check the networking requirements with AWS documentation [here](https://docs.aws.amazon.com/mwaa/latest/userguide/networking-about.html).  
   Alternatively, you can create a new VPC using a cloudformation template from this article's git source code: cloudformation\010_vpc.yaml:
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

### 2. Create S3 bucket for Airflow Cluster and upload sample DAGs and requirements.txt files there

2.1 S3 creation via CloudFormation Stack:
```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-015-s3"

  aws cloudformation deploy \
    --template-file cloudformation/015_s3.yaml \
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

  aws s3 sync airflow/ s3://${s3_bucket_name}/ --delete
```   

### 3. Create Managed Airflow cluster and its IAM Role

Notes:
- Airflow cluster requires security_group_id and private subnets ids as parameters. If you've created VPC using a template in step 1 - first commands of a script will pick the values automatically. Otherwise, replace cloudformation deploy command parameters with your values.

```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-020-mwaa"

    ################################################################################
    # get outputs (from CloudFormation VPC Stack)
    output=$(aws cloudformation list-exports)

    # Extract the values for the specific items using jq
    private_subnets_csv=$(echo "$output" | jq -r '.Exports[] | select(.Name == "vpc-mwaa-secrets-demo-private-subnets-csv") | .Value')
    security_group_id=$(echo "$output" | jq -r '.Exports[] | select(.Name == "vpc-mwaa-secrets-demo-security-group-id") | .Value')
    ################################################################################

  aws cloudformation deploy \
    --template-file cloudformation/020_mwaa.yaml \
    --stack-name $stack_name \
    --no-fail-on-empty-changeset \
    --parameter-overrides ProjectName=$project_name MWAAS3Bucket=$s3_bucket_name MWAASecurityGroupIds=$security_group_id MWAASubnetIds=$private_subnets_csv \
    --capabilities CAPABILITY_NAMED_IAM
```   

This cloudformation stack contains:
- IAM policy which allows MWAA environment to read values of stored secrets (Requirement #1 mentioned above).
![IAM Policy to access Secrets Manager values](images/iam_policy_secrets.png)

- MWAA Environment definition with the following important settings:
![IAM Policy to access Secrets Manager values](images/mwaa_definition.png)
    1. Reference to file requirements.txt containing list of database interaction libraries (Requirement #2 mentioned above)
    2. Declaring Secrets Manager as a backend used for storing/retrieving connection and variable values
    3. Local OS variables definition which is discussed in next section for working with Variables

Sample content of **requirements.txt** file (assuming we are going to use MySQL and PostreSQL databases):
```
apache-airflow[mysql]
apache-airflow[postgres]
```

### 4. Create sample secrets

<<todo:>>
!! Replace 030_secrets.yaml values with DUMMY data

<<todo:>>
1. Add screenshot of secrets
2. Explain difference between URI and JSON format
3. Mention JSON available since 2.3.1
4. Formats can be used interchangebly


## Using connections - sample DAGs

<<todo:>>
1. demo_mysql_connection_dag.py - Show MySQLOperator and PythonOperator
2. refer to demo_postgresql_connection_dag.py - the same implemented for PostgreSQL

## Using Variable values (Secrets / OS local variable)

<<todo:>> All resources created in previous steps

### Retrieving variable value from Secrets Manager

<<todo:>>
0. screenshots how they are defined
1. demo_variable_secrets_dag.py
3. Usage result

### Retrieving environment variable value

<<todo:>>
0. screenshots how they are defined
1. demo_env_variable_dag.py
2. All CAPS and "_" sign
3. Usage result

### Variable comparison

<<todo:>>
1. Secrets
  pros: can change value on the fly
  cons: 

2. OS Variable
  pros:
  cons: change values -> Update env



## Considerations when using Connections and Variables in Secrets Manager

<<todo:>> - pricing

## Clean Up

<<todo:>>

### x. Delete VPC Stack

```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-010-vpc"

  aws cloudformation delete-stack --stack-name $stack_name
  aws cloudformation wait stack-delete-complete --stack-name $stack_name
```  