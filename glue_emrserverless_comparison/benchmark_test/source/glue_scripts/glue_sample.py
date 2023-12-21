import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

print('Running pure Spark option')

# Fetching arguments
args = getResolvedOptions(sys.argv, ['s3_bucket_name'])
s3_bucket_name = args['s3_bucket_name']

print('Hello from GLUE PySpark!!!')
print('S3 Bucket Name: ' + s3_bucket_name)