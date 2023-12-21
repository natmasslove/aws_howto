import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

print('Converts csv -> pq data. Only for 1 csv file')

# Fetching arguments
args = getResolvedOptions(sys.argv, ['s3_bucket_name','input_path','output_path'])
s3_bucket_name = args['s3_bucket_name']
input_path = args['input_path']
output_path = args['output_path']

# Initializing Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Input and output paths
full_input_path = f"s3://{s3_bucket_name}/{input_path}"
full_output_path = f"s3://{s3_bucket_name}/{output_path}"

print(f'Reading CSV file from {full_input_path}')
# Reading the CSV file
df = spark.read.csv(full_input_path, header=True, inferSchema=True)

print(f'Writing data to {full_output_path}')
# Writing the data in Parquet format
df.write.mode("overwrite").parquet(full_output_path)

print('Done')