from datetime import datetime
import time
import boto3
from helpers.cloudformation import get_stack_outputs
from helpers.s3_helper import upload_file_to_s3
from helpers.emr_serverless import start_job_run, watch_job_run
import logging
from time import strftime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)  # so we see logged messages in console when debugging

stack_name = "cf-emrsrvless-demo"

#################################################################
outputs = get_stack_outputs(stack_name)

application_id = outputs["EMRServerlessApplicationId"]
execution_role_arn = outputs["EMRServerlessRoleArn"]
s3_bucket = outputs["EMRServerlessS3Bucket"]

#################################################################
# copy the script to S3
paths = ["spark_scripts/sample_convert.py", "sample_data/sample.csv"]
for path in paths:
    upload_file_to_s3(path, s3_bucket, path)

#################################################################
emr_client = boto3.client("emr-serverless")

script_path = f"s3://{s3_bucket}/{paths[0]}"

strtime = datetime.now().strftime("%Y%m%d%H%M%S")
run_name = f"{paths[0]}-{strtime}"
arguments = [s3_bucket]

# Starting Job Run
job_run_id, response = start_job_run(
    emr_client,
    application_id,
    script_path,
    arguments,
    run_name,
    execution_role_arn,
    logger,
)

# Waiting for Job Run to Complete and collect stats
start = time.perf_counter()
totalResourceUtilization, totalExecutionDurationSeconds = watch_job_run(
    emr_client, application_id, job_run_id, logger
)
end = time.perf_counter()

# Print out Run stats
print(f"Total Resource Utilization: {totalResourceUtilization}")
print(f"Total Execution Duration: {totalExecutionDurationSeconds} seconds")
print(f"Total Execution Time: {end - start:0.4f} seconds")
