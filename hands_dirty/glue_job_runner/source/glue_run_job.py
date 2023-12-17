import time
import logging

import boto3

from helpers.glue import start_job_run, watch_job_run
from helpers.cloudformation import get_stack_outputs
from helpers.s3_helper import upload_file_to_s3


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)  # so we see logged messages in console when debugging

file_handler = logging.FileHandler("run_job.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#################################################################
stack_name = "cf-glue-runner-sample"
cf_outputs = get_stack_outputs(stack_name)

s3_bucket = cf_outputs["GlueSampleS3Bucket"]

#################################################################
# copy the script to S3
paths = ["glue_scripts/sample_convert.py", "sample_data/sample.csv"]
for path in paths:
    upload_file_to_s3(path, s3_bucket, path)

#################################################################

glue_client = boto3.client("glue")

job_name = "gluej-runner-sample-job"
arguments = {
    "--s3_bucket_name" : s3_bucket
}

start = time.perf_counter()

# Starting Job Run
args = {
    "glue_client" : glue_client,
    "job_name" : job_name,
    "arguments" : arguments,
    "logger" : logger,
}
job_run_id, response = start_job_run(**args)

logger.info(response)

# Waiting for Job Run to Complete and collect stats
args = {
    "glue_client" : glue_client,
    "job_name" : job_name,
    "job_run_id" : job_run_id,
    "logger" : logger,
}
output = watch_job_run(**args)
    

end = time.perf_counter()

formatted_output = output #json.dumps(output, indent=4)

# Print out Run stats
print(f"Output:\n{formatted_output}")
print(f"Total Running Time: {end - start:0.4f} seconds")
