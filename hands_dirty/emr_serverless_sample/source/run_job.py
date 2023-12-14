from datetime import datetime
import boto3
from helpers.cloudformation import get_stack_outputs
from helpers.s3_helper import upload_file_to_s3
from helpers.emr_serverless import watch_job_run
import logging
from time import strftime

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')   
handler.setFormatter(formatter)
logger.addHandler(handler)  # so we see logged messages in console when debugging

stack_name = 'cf-emrsrvless-sample'

#################################################################
outputs = get_stack_outputs(stack_name)

application_id = outputs['EMRServerlessApplicationId']
execution_role_arn = outputs['EMRServerlessRoleArn']
s3_bucket = outputs['EMRServerlessS3Bucket']

#################################################################
# copy the script to S3
paths = ['spark_scripts/sample_convert.py', 'sample_data/sample.csv']
for path in paths:    
    upload_file_to_s3(path, s3_bucket, path)


#################################################################
emr_client = boto3.client('emr-serverless')

job_driver = {
    "sparkSubmit": {
        "entryPoint": f"s3://{s3_bucket}/{paths[0]}",
        "sparkSubmitParameters": "--conf spark.hadoop.hive.metastore.client.factory.class=com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
    }
}
strtime = datetime.now().strftime('%Y%m%d%H%M%S')
run_name = f"spark-run-{strtime}"
configuration_overrides = {
    "monitoringConfiguration": {
        "managedPersistenceMonitoringConfiguration": {
            "enabled": True
        }
    }
}


response = emr_client.start_job_run(
    applicationId=application_id,
    executionRoleArn=execution_role_arn,
    jobDriver=job_driver,
    configurationOverrides=configuration_overrides,
    name=run_name
)

job_run_id = response['jobRunId']
print(f"Job Run started. Job Run ID: {job_run_id}")
print(response)

watch_job_run(emr_client, application_id, job_run_id, logger)