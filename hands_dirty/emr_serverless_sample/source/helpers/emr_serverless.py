import time


def start_job_run(
    emr_client,
    application_id,
    script_path,
    arguments,
    run_name,
    execution_role_arn,
    logger,
):
    job_driver = {
        "sparkSubmit": {
            "entryPoint": script_path,
            "entryPointArguments": arguments,
            "sparkSubmitParameters": "--conf spark.hadoop.hive.metastore.client.factory.class=com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory",
        }
    }
    configuration_overrides = {
        "monitoringConfiguration": {
            "managedPersistenceMonitoringConfiguration": {"enabled": True}
        }
    }

    response = emr_client.start_job_run(
        applicationId=application_id,
        executionRoleArn=execution_role_arn,
        jobDriver=job_driver,
        configurationOverrides=configuration_overrides,
        name=run_name,
    )

    job_run_id = response["jobRunId"]
    logger.info(f"Job Run started. Job Run ID: {job_run_id}")
    return job_run_id, response


def watch_job_run(emr_client, application_id, run_id, logger):
    status = None

    response = ""
    # Waiting for Job Run to Complete (reach final state)
    while status not in ["SUCCESS", "FAILED"]:
        response = emr_client.get_job_run(applicationId=application_id, jobRunId=run_id)
        status = response["jobRun"]["state"]
        logger.info(status)
        time.sleep(2)

    i = 0
    # Waiting until execution stats are available (they don't appear in response immediately)
    while (
        "totalResourceUtilization" not in response["jobRun"]
        or "totalExecutionDurationSeconds" not in response["jobRun"]
    ):
        response = emr_client.get_job_run(applicationId=application_id, jobRunId=run_id)
        time.sleep(2)
        i += 1
        if i > 200:
            break
        logger.info(f"Waiting for totalResourceUtilization to be populated.")

    totalResourceUtilization = response["jobRun"]["totalResourceUtilization"]
    totalExecutionDurationSeconds = response["jobRun"]["totalExecutionDurationSeconds"]

    return totalResourceUtilization, totalExecutionDurationSeconds
