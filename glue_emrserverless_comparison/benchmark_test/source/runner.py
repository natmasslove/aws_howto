import os
from datetime import datetime
import time
import boto3
from helpers.common import get_logger
from helpers.cloudformation import get_stack_outputs
from helpers.s3_helper import upload_file_to_s3
from helpers.emr_serverless import start_job_run, watch_job_run
from time import strftime
import json

STACK_NAME = "cf-glue-vs-emr-serverless"
SCRIPT_PATH = script_dir = os.path.dirname(os.path.abspath(__file__))

#################################################################
outputs = get_stack_outputs(STACK_NAME)

s3_bucket = outputs["BenchmarkTestS3Bucket"]
# EMR
application_id = outputs["EMRServerlessApplicationId"]
execution_role_arn = outputs["EMRServerlessRoleArn"]
# Glue


#################################################################
# EMR Flow
logger = get_logger(log_name="emrserverless")

script_name = "emrserverless_scripts/emr_sample.py"
upload_file_to_s3(os.path.join(SCRIPT_PATH, script_name), s3_bucket, script_name)

emr_client = boto3.client("emr-serverless")

strtime = datetime.now().strftime("%Y%m%d%H%M%S")
run_name = f"{script_name}-{strtime}"
arguments = [s3_bucket]

logger.info(f"Running script {script_name}, using arguments: [{', '.join(arguments)}]")

# this is optional - just to demonstrate how you can change compute capacity allocation for the job run
# you also can leave it empty sparkSubmitParameters = {}
sparkSubmitParameters = {
    "spark.hadoop.hive.metastore.client.factory.class" : "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory",    
    "spark.executor.instances" : "1",
    "spark.dynamicAllocation.initialExecutors" : "1",
    "spark.dynamicAllocation.maxExecutors" : "1",
    "spark.executor.cores" : "2",
    "spark.executor.memory" : "8G",
}

start = time.perf_counter()

# Starting Job Run
job_run_id, response = start_job_run(
    emr_client,
    application_id,
    script_name,
    arguments,
    run_name,
    execution_role_arn,    
    logger,
    sparkSubmitParameters,
)

logger.info(response)

# Waiting for Job Run to Complete and collect stats
output = watch_job_run(
    emr_client, application_id, job_run_id, logger
)

end = time.perf_counter()

formatted_output = json.dumps(output, indent=4)

# Print out Run stats
print(f"Output:\n{formatted_output}")
print(f"Total Running Time: {end - start:0.4f} seconds")
