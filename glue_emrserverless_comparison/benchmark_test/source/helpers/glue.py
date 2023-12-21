import boto3
from datetime import datetime
import time
from urllib.parse import urlparse

from helpers.s3_helper import upload_file_to_s3

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

def get_job_script_location(glue_client, job_name):
    response = glue_client.get_job(JobName=job_name)
    script_location = response["Job"]["Command"]["ScriptLocation"]
    return script_location

def run_test(glue_client, local_script_fullpath, job_name):
    print('in glue run test')
    print(glue_client, local_script_fullpath, job_name)

    s3_script_location = get_job_script_location(glue_client, job_name)
    # split s3_script_location into bucket and key
    s3_path_parts = urlparse(s3_script_location, allow_fragments=False)
    s3_bucket_name, s3_prefix = s3_path_parts.netloc, s3_path_parts.path.lstrip("/")
    print(s3_script_location, s3_bucket_name, s3_prefix)

    upload_file_to_s3(local_script_fullpath, s3_bucket_name, s3_prefix)
    pass
    # #################################################################
    # # copy the script to S3
    # paths = ["glue_scripts/sample_convert.py", "sample_data/sample.csv"]
    # for path in paths:
    #     upload_file_to_s3(path, s3_bucket, path)

    # #################################################################

    # glue_client = boto3.client("glue")

    # job_name = "gluej-runner-sample-job"
    # arguments = {
    #     "--s3_bucket_name" : s3_bucket
    # }

    # start = time.perf_counter()

    # # Starting Job Run
    # args = {
    #     "glue_client" : glue_client,
    #     "job_name" : job_name,
    #     "arguments" : arguments,
    #     "logger" : logger,
    # }
    # job_run_id, response = start_job_run(**args)

    # logger.info(response)

    # # Waiting for Job Run to Complete and collect stats
    # args = {
    #     "glue_client" : glue_client,
    #     "job_name" : job_name,
    #     "job_run_id" : job_run_id,
    #     "logger" : logger,
    # }
    # output = watch_job_run(**args)
        

    # end = time.perf_counter()

    # formatted_output = output #json.dumps(output, indent=4)

    # # Print out Run stats
    # print(f"Output:\n{formatted_output}")
    # print(f"Total Running Time: {end - start:0.4f} seconds")

        