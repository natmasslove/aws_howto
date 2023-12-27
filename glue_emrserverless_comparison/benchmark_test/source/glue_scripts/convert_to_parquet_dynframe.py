import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

print('Converts csv -> pq data.')

# Fetching arguments
args = getResolvedOptions(sys.argv, ['s3_bucket_name','input_path','output_path'])
s3_bucket_name = args['s3_bucket_name']
input_path = args['input_path']
output_path = args['output_path']
print(f'Using s3 bucket name {s3_bucket_name}\n Reading from {input_path}\n Writing to {output_path}\n')

# Initializing Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)

# Input and output paths
full_input_path = f"s3://{s3_bucket_name}/{input_path}"
full_output_path = f"s3://{s3_bucket_name}/{output_path}"

print(f'Reading CSV file from {input_path}')

# Reading the CSV file into a DynamicDataFrame
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [full_input_path]},
    format="csv",
    format_options={"withHeader": True}
)

print(f'Writing data to {output_path}')

# Writing the data in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={"path": full_output_path},
    format="parquet",
    format_options={"mode": "overwrite"}
)

print('Done')