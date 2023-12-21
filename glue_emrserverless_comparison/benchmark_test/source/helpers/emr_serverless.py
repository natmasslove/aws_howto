import time
from datetime import datetime

def start_job_run(
    emr_client,
    application_id,
    script_path,
    arguments,
    run_name,
    execution_role_arn,
    logger,
    sparkSubmitParameters = None,    
):
    if sparkSubmitParameters is None:
        sparkSubmitParameters = {
            "spark.hadoop.hive.metastore.client.factory.class" : "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory",
        }

    sparkSubmitParameters_str = " --conf " + " --conf ".join(f"{k}={v}" for k, v in sparkSubmitParameters.items())
    print(f"sparkSubmitParameters_str: {sparkSubmitParameters_str}")

    job_driver = {
        "sparkSubmit": {
            "entryPoint": script_path,
            "entryPointArguments": arguments,
            "sparkSubmitParameters": sparkSubmitParameters_str,
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
    state_durations = {}  # Dictionary to store durations for each state
    last_state_change = datetime.now()  # Initialize the time for state change
    current_state = None

    response = ""
    # Waiting for Job Run to Complete (reach final state)
    while current_state not in ["SUCCESS", "FAILED"]:
        response = emr_client.get_job_run(applicationId=application_id, jobRunId=run_id)
        new_state = response["jobRun"]["state"]

        if new_state != current_state:
            current_time = datetime.now()
            if current_state is not None:
                duration = (current_time - last_state_change).total_seconds()
                state_durations[current_state] = duration
                logger.info(f"State {current_state}: {duration} seconds")

            last_state_change = current_time
            current_state = new_state

        logger.info(new_state)
        time.sleep(2)

    # Add the duration for the final state
    duration = (datetime.now() - last_state_change).total_seconds()
    state_durations[current_state] = duration    

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
            raise Exception("Can't retrieve total source utilization stats")
        logger.info(f"Waiting for totalResourceUtilization to be populated.")

    totalResourceUtilization = response["jobRun"]["totalResourceUtilization"]
    totalExecutionDurationSeconds = response["jobRun"]["totalExecutionDurationSeconds"]

    output = {
        "state_durations" : state_durations,
        "totalResourceUtilization" : totalResourceUtilization,
        "totalExecutionDurationSeconds" : totalExecutionDurationSeconds,
    }

    return output
