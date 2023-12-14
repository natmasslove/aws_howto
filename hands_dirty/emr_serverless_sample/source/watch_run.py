import boto3
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')   
handler.setFormatter(formatter)
logger.addHandler(handler)  # so we see logged messages in console when debugging



emr_client = boto3.client('emr-serverless')

application_id = "00ffgfgdaom1gf15"
run_id = "00ffgfu12c5i3816"

status = None

response = ""
while status not in ["SUCCEEDED","FAILED"]:
    response = emr_client.get_job_run(
        applicationId=application_id,
        jobRunId=run_id
    )
    status = response["jobRun"]["state"]
    logger.info(status)
    time.sleep(2)

print(response)