# Goals:

1. Create a snippet to create a Glue table via CloudFormation template
2. Check functionality for updating Glue table S3 location (switching between folders)

# Steps:

1. Run scripts/010_resources.sh - Cloudformation Stack that creates s3 bucket (for sample data)
2. Run scripts/020_copy_datasets.sh - Copies 2 csv files: dataset_a and dataset_b (generated sample data, same structure both) to S3 bucket, different folders
3. Run scripts/020_resources.sh - Cloudformation Stack to create Glue Database and Glue Table in Data Catalog.  
Initially table references to "dataset_a".

4. Run Athena query 
```sql
select * from sample_table limit 3 
```
Column "version" contains value "Dataset A" - it means Glue table references to dataset_a

5. Run python script: python/switch_table_location.py. It switches Glue table between data dataset_a and dataset_b each run.

6. Run the same Athena query.  
Column "version" now contains value "Dataset B" - referencing dataset_b

# Clean Up:

Run shell script /scripts/delete/delete_all.sh.  
It will delete all resources created in this demo.