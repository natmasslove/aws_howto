import sys
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.dynamicframe import DynamicFrame

print('Running dynamic frame option')

# Fetching arguments
args = getResolvedOptions(sys.argv, ['s3_bucket_name'])
s3_bucket_name = args['s3_bucket_name']

# Initializing Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)

# Input and output paths
input_path = f"s3://{s3_bucket_name}/sample_data/sample.csv"
output_path = f"s3://{s3_bucket_name}/sample_data/output_data.parquet"

print(f'Reading CSV file from {input_path}')

# Reading the CSV file into a DynamicDataFrame
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [input_path]},
    format="csv",
    format_options={"withHeader": True}
)

print(f'Writing data to {output_path}')

# Writing the data in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={"path": output_path},
    format="parquet",
    format_options={"mode": "overwrite"}
)

print('Done')