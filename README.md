# Intro

This project provides a collection of helpful tips and tricks for working with AWS.  
Each "how-to" includes practical code examples, CloudFormation templates, and Bash scripts that can help simplify the deployment process.

# How-To List:

This section includes articles describing solution to the problems which I think either not very well documented (at the moment when I wrote the article 😃 ) or require excessive amount of experimentation to make things work.  

Here I wanted to provide solutions which you can easily take and adjust for your needs with minimal efforts.

* [Guide for setting up Glue Jobs and Connections to work with Snowflake and SAP](glue_connections_snowflake_sap/README.md)
* [How to setup and use connections and variables in AWS managed Apache Airflow](mwaa_connections_and_vars/README.md)
* [How to accelerate your Glue Job development with Glue Interactive Sessions](glue_interactive_sessions/README.md)

# Getting-Hands-Dirty section:

Here I put small "projects" where I either explore new functionalities or create snippets to be re-used by "future myself" (or anyone else, of course 😃 )

* [How to use your own Python library in **Pythonshell** Glue Job](handson/20230704_glue_pythonshell_add_your_lib/README.md)
* [Experiments with switching Athena table between two s3 locations](handson/20230615_glue_table_cf_snippet_and_altering_location/README.md)
* [How Athena works with INSERT INTO commands for various table formats](handson/20230712_testing_athena_insert/README.md)
* [Timestream samples and research](handson/timestream_samples/README.md)
* [EMR Serverless samples](handson/emr_serverless_sample/README.md)


