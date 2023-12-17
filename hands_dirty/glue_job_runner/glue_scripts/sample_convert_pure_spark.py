import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

print('Running pure Spark option')

# Fetching arguments
args = getResolvedOptions(sys.argv, ['s3_bucket_name'])
s3_bucket_name = args['s3_bucket_name']

# Initializing Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Input and output paths
input_path = f"s3://{s3_bucket_name}/sample_data/sample.csv"
output_path = f"s3://{s3_bucket_name}/sample_data/output_data.parquet"

print(f'Reading CSV file from {input_path}')
# Reading the CSV file
df = spark.read.csv(input_path, header=True, inferSchema=True)

print(f'Writing data to {output_path}')
# Writing the data in Parquet format
df.write.mode("overwrite").parquet(output_path)

print('Done')