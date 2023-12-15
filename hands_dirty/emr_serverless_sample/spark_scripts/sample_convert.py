
from pyspark.sql import SparkSession
import os
import sys

if len(sys.argv) < 2:
    print("Usage: script.py <S3_BUCKET_NAME>")
    sys.exit(-1)

# gets S3 bucket name from spark job params
s3_bucket_name = sys.argv[1]
print(f'Using s3 bucket name {s3_bucket_name}')

# Initialize Spark session
spark = SparkSession.builder.appName("CSV to Parquet").getOrCreate()

# Define file paths
s3_folder = f"s3://{s3_bucket_name}/sample_data/"
csv_file = s3_folder + "sample.csv"
parquet_file = s3_folder + "output_data.parquet"

print(f'Reading CSV file from {csv_file}')
# Read CSV file
df = spark.read.csv(csv_file, header=True, inferSchema=True)

print(f'Writing Parquet file to {parquet_file}')
# Write to Parquet
df.write.mode('overwrite').parquet(parquet_file)

print('Exiting')
# Stop the Spark session
spark.stop()
