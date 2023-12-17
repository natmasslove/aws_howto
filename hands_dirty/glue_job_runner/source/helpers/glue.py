import boto3
from datetime import datetime
import time

States_Success = ["SUCCEEDED"]
States_Failure = ["FAILED", "ERROR", "TIMEOUT", "STOPPED"]
Final_States = States_Success + States_Failure

def start_job_run(glue_client, job_name, arguments, logger):
    response = glue_client.start_job_run(JobName=job_name, Arguments=arguments)
    job_run_id = response["JobRunId"]
    logger.info(f"Job Run started. Job Run ID: {job_run_id}")
    return job_run_id, response                     


def watch_job_run(glue_client, job_name, job_run_id, logger):
    state_durations = {}  # Dictionary to store durations for each state
    last_state_change = datetime.now()  # Initialize the time for state change
    current_state = None

    response = ""
    # Waiting for Job Run to Complete (reach final state)
    while current_state not in Final_States:
        response = glue_client.get_job_run(JobName=job_name, RunId=job_run_id)
        new_state = response["JobRun"]["JobRunState"]

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

    output = {
        "state_durations" : state_durations,
        "response" : response,
    }

    return output



    