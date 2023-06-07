
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

Full source code is stored in Git Repository: https://github.com/natmasslove/aws_howto/tree/mwaa_connections_and_vars/mwaa_connections_and_vars

## Secrets manager-based Connections: How it works

A diagram below represents on a high-level how connections are referenced in Airflow DAGs and how connection details are retrieved from AWS Secrets manager.  
This requires setting airflow cluster and deploying other AWS resources properly.  
In this article we demonstrate the process providing examples and the source code.

![High-level description](images/high-level-conn.png)


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
Let's create sample secrets which we can use:
*Note: if you have a MySQL database to experiment with - please change sample parameter values with actual ones*
```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-025-secrets-mysql-and-var"

  aws cloudformation deploy \
    --template-file cloudformation/025_secrets_mysql_and_var.yaml \
    --stack-name $stack_name \
    --no-fail-on-empty-changeset \
    --parameter-overrides ProjectName=$project_name DBHost=sample_host DBLogin=sample_user DBPassword=sample_password DBDatabase=sample_dbname
```

Cloudformation stack creates 3 resources:
1. Secret containing connection to MySQL database in URI format
2. Secret in JSON format
3. Secret containing value for variable - it will be used in "Variables" section.

#### **Secret String Format**

Two secrets created (URI and JSON format) are equivalent and can be used interchangeably.
Here we create both only for demonstrational purposes.

URI Format:
```
mysql://login:password@DBHost:3306/database
```

JSON Format:
```json
  {
      "conn_type": "mysql",
      "login"    : "login",
      "password" : "password",
      "host"     : "DBHost",
      "database" : "database",
      "port"     : 3306
  }
```

When choosing which format to use consider the following:
- JSON format for storing credentials available starting from Airflow version 2.3.0
- JSON format tends to be more readable in our opinion. Also, it might be more friendly for other secret value consumers (other scripts or services which might need to retrieve DB credentials)

More on secrets format you can read in [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html).

*Note: If you prefer using PostgreSQL database - there's an alternative template for it: cloudformation/030_secrets_postgresql.yaml. The differences are **conn_type** value and default DB port*

#### **Secrets Naming**

That's how secret names are defined:  
![Secret Names](images/secret_name.png)

Secret names start with a prefix which was defined in Airflow Environment creation template:  
![Secrets Prefix](images/secret_prefix_mwaa.png)

As a result in DAGs these connections can be refered by name, respectively, as:
- **aurora_mysql_uri**
- **aurora_mysql_json**

## Using connections - sample DAGs

Now let's log into our MWAA environment and test connections in our DAGs.  
The sample DAG we have for the test is "demo_connection_mysql" (and if you database of preference in PostreSQL, you can use "demo_connection_postgresql" instead. Differences are minimal).

*Note: Full source code of DAGs can be found in git: airflow\dags*

![dag list](images/demo_mysql_dag.png)

DAG contains three operators:

![dag operators](images/demo_dag_operators.png)

1. **mysql_uri_connection** - which demonstrates using MySQLOperator to run "Create Table command" using connection defined in URI format

```python
    mysql_uri_operator = MySqlOperator(
        task_id='mysql_uri_connection',
        mysql_conn_id = 'aurora_mysql_uri', # refers to secret named <connection_prefix>/aurora_mysql_uri
        sql=CREATE_SQL
    )
```

2. **execute_sql_json_connection** - uses MySQLHook inside PythonOperator to execute simple select using connection defined in JSON format (as you might remember, both URI and JSON format and interchangeable)

```python
    conn_id = "aurora_mysql_json" # refers to secret named <connection_prefix>/aurora_mysql_json
    sql = SELECT_SQL

    result = []
    mysql_hook = MySqlHook(mysql_conn_id=conn_id)
    ...
```

3. **get_connection** - retrieves and outputs both URI and JSON connections to prove they result in the same connection properties
![get_connection_output](images/get_connection_output.png)

## Using Variable values (Secrets / OS local variable)

Now let's take a look at several ways to define variables in Airflow.

![High-level description](images/high-level-variables.png)

The first one is to define those using AWS Secrets Manager (very similar to working with connection we described above).  

Another method is to define OS environment variables, which is more suitable for rarely changing values (one of real-life examples -
is to define environment-name (dev/qa/prod)).

If you have followed cluster set up steps from previous section, all variables are already ready to use.
Let's proceed and test those.

### Retrieving variable value from Secrets Manager

MWAA cluster settings done in cloudformation\020_mwaa.yaml (variables_prefix):
```yaml
      AirflowConfigurationOptions:
        secrets.backend: airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
        secrets.backend_kwargs: !Sub '{"connections_prefix" : "${ProjectName}/connections", "variables_prefix" : "${ProjectName}/variables"}'
```

Test variable is created in cloudformation\025_secrets_mysql_and_var.yaml:
```yaml
  SecretMWAATestVariable:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub '${ProjectName}/variables/test_variable'
      SecretString: This is a Value of test variable (stored in secrets manager)
```

Now let's retrieve the value using demo_variable_secrets DAG:

![demo_variable_secrets_dag](images/demo_variable_secrets_dag.png)

```python
  def print_vars_from_secret():
      var_names = ['test_variable'] # searches for secret named "${ProjectName}/variables/test_variable"
      for item in var_names:
          value = Variable.get(item)
          print(f"---> {item} : {value}")
```

The task output looks like this:
```
[2023-06-07, 20:38:34 UTC] {{logging_mixin.py:137}} INFO - ---> test_variable : This is a Value of test variable (stored in secrets manager)
```

As easy as that!

### Retrieving environment variable value

We have defined two environment variables whilst creating the cluster (cloudformation/020_mwaa.yaml):
```yaml
      AirflowConfigurationOptions:
        ...
        os_var.variable1: value1
        env.variable2: 2023
```

Now let's access those running demo_variable_env DAG:
```python
  def print_defined_vars():
      var_names = ['AIRFLOW__OS_VAR__VARIABLE1','AIRFLOW__ENV__VARIABLE2']

      for item in var_names:
          value = os.environ[item]
          print(f"---> {item} : {value}")
```
**Please note the name change:**
- CloudFormation template:
  - os_var.variable1
  - env.variable2
- Accessing from DAG ("AIRFLOW_" prefix & all uppercase & "." is replaced by "__")
  - AIRFLOW__OS_VAR__VARIABLE1
  - AIRFLOW__ENV__VARIABLE2

The output:
```
[2023-06-07, 20:51:06 UTC] {{logging_mixin.py:137}} INFO - ---> AIRFLOW__OS_VAR__VARIABLE1 : value1
[2023-06-07, 20:51:06 UTC] {{logging_mixin.py:137}} INFO - ---> AIRFLOW__ENV__VARIABLE2 : 2023
```

### Methods comparison

Variables stored in AWS Secrets Manager provide more flexibility as you can change its the value just by modifying the secret.

While for environment variable change you need to update cluster settings, which is time-consuming operation (taking 20-30 minutes).

The downside of secret-based variables is the fact you are charged for each secret stored.


## Considerations when using Connections and Variables in Secrets Manager

Please don't forget your are charged for storing and accessing each secret.
Current price is $0.40 per secret per month and $0.05 per 10 000 API calls (pricing might be subject to change, so check the actual charges in [AWS Documentation] (https://aws.amazon.com/secrets-manager/pricing/?nc1=h_ls) )

## Clean Up

Here are the step to clean up demonstrational resources we've created in this guide:

### 1. Delete secrets

```bash
export project_name="mwaa-secrets-demo"
aws secretsmanager delete-secret --secret-id ${project_name}/connections/aurora_mysql_uri --force-delete-without-recovery 
aws secretsmanager delete-secret --secret-id ${project_name}/connections/aurora_mysql_json --force-delete-without-recovery 
aws secretsmanager delete-secret --secret-id ${project_name}/connections/aurora_postgresql_uri --force-delete-without-recovery 
aws secretsmanager delete-secret --secret-id ${project_name}/connections/aurora_postgresql_json --force-delete-without-recovery 
aws secretsmanager delete-secret --secret-id ${project_name}/variables/test_variable --force-delete-without-recovery 

export stack_name="cfrm-${project_name}-025-secrets-mysql-and-var"

  aws cloudformation delete-stack --stack-name ${stack_name}
  aws cloudformation wait stack-delete-complete --stack-name ${stack_name}

export stack_name="cfrm-${project_name}-030-secrets-postgresql"

  aws cloudformation delete-stack --stack-name ${stack_name}
  aws cloudformation wait stack-delete-complete --stack-name ${stack_name}  
```    

*Note: we included explicit Secret deletion (not via CloudFormation) with "force-delete-without-recovery".
It makes possible to delete and recreate sample stacks multiple times.  
Otherwise, AWS performs "soft delete" of the secret and it will lead to an error if you try to create stack within next 30 days.*


### 2. Delete Airflow Cluster

```bash
export project_name="mwaa-secrets-demo"
export stack_name="cfrm-${project_name}-020-mwaa"

  aws cloudformation delete-stack --stack-name ${stack_name}
  aws cloudformation wait stack-delete-complete --stack-name ${stack_name}
```    

### x. Delete VPC Stack

```bash
  export project_name="mwaa-secrets-demo"
  export stack_name="cfrm-${project_name}-010-vpc"

  aws cloudformation delete-stack --stack-name $stack_name
  aws cloudformation wait stack-delete-complete --stack-name $stack_name
```  