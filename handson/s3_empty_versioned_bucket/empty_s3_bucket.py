import boto3
import argparse
from botocore.exceptions import ClientError

def empty_s3_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    print(bucket.object_versions)
     
    
    # Delete all versions of all objects in the bucket
    try:
        bucket.object_versions.delete()
        print(f"All versions of all objects in the bucket '{bucket_name}' have been deleted.")
    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")

parser = argparse.ArgumentParser(description='Empty an S3 bucket with versioning enabled.')
parser.add_argument('--bucket_name', type=str, required=True, help='Name of the S3 bucket to be emptied')

args = parser.parse_args()
print(args.bucket_name)

empty_s3_bucket(args.bucket_name)