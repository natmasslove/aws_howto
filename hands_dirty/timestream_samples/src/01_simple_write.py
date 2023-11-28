import time
import boto3
import uuid
from lib.aws.timestream_manager import TimestreamTableWriter

# These tests show how to insert more than 100 records (uses TimestreamTableWriter batched method to write)

DB_NAME = "timestream-sample-db"
TABLE_NAME = "poc-table-01-batch-write"

ts_client = boto3.client("timestream-write")


def prepare_records(number_of_records: int):
    records = []

    epoch_seconds = time.time()

    for i in range(0, number_of_records):
        dimensions = [
            {
                "Name": "dim_one",
                "Value": "value_one",
            },
            {
                "Name": "dim_two",
                "Value": str(uuid.uuid1()),
            },
        ]

        record_time = TimestreamTableWriter.epoch_milliseconds_str(
            epoch_seconds=epoch_seconds
        )

        records.append(
            {
                "Dimensions": dimensions,
                "MeasureName": "measure_1",
                "MeasureValue": str(i),
                "MeasureValueType": "BIGINT",
                "Time": record_time,
            }
        )

    print(f"Generated {len(records) } records")
    return records


#########################################################
print(
    "STEP 1. prepare batch of <100 records and try to write those using 'simple' method, without splitting into batches"
)
records = prepare_records(77)
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records_simple(records)  # naive method
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = SUCCESS

#########################################################
print(
    "STEP 2. prepare batch of >100 records and try to write those using 'simple' method, without splitting into batches"
)
records = prepare_records(110)
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records_simple(records)  # naive method
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = Exception "failed to satisfy constraint: Member must have length less than or equal to 100."


#########################################################
print(
    "STEP 3. prepare batch of >100 records and try to write those using batched method, where we split records into batches"
)
records = prepare_records(110)
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records(records)  # changed method
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = SUCCESS
