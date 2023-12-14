import boto3
from botocore.exceptions import ClientError

from pyspark.sql import SparkSession

def get_current_aws_account():
    try:
        sts_client = boto3.client('sts')
        account_id = sts_client.get_caller_identity()["Account"]
        return account_id
    except ClientError as error:
        print(f"An error occurred: {error}")
        return None

# Initialize Spark session
spark = SparkSession.builder.appName("CSV to Parquet").getOrCreate()

# Define file paths
s3_folder = f"s3://s3-emr-serverless-demo-{get_current_aws_account()}/sample_data/"
csv_file = s3_folder + "sample.csv"
parquet_file = s3_folder + "output_data.parquet"

# Read CSV file
df = spark.read.csv(csv_file, header=True, inferSchema=True)

# Write to Parquet
df.write.parquet(parquet_file)

# Stop the Spark session
spark.stop()
