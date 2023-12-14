import time

def watch_job_run(emr_client, application_id, run_id, logger):
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
    return response