import time
import boto3
import uuid
from lib.aws.timestream_manager import TimestreamTableWriter

# This provides snippets on how to works with attributes having the same
# value for all records we are going to write

DB_NAME = "timestream-sample-db"
TABLE_NAME = "poc-table-04-common-attributes"

ts_client = boto3.client("timestream-write")


def prepare_records():
    records = []

    common_dimensions = [{"Name": "dim_one", "Value": "common_value"}]

    epoch_seconds = time.time()
    common_record_time = TimestreamTableWriter.epoch_milliseconds_str(
        epoch_seconds=epoch_seconds
    )

    # common_attributes defined
    common_attributes = {"Dimensions": common_dimensions, "Time": common_record_time}

    for i in range(0, 10):
        dimensions = [
            {
                "Name": "dim_two",
                "Value": str(uuid.uuid1()),
            },
        ]

        records.append(
            {
                "Dimensions": dimensions,
                "MeasureName": "measure_1",
                "MeasureValue": str(i),
                "MeasureValueType": "BIGINT"
            }
        )

    return common_attributes, records


common_attributes, records = prepare_records()

#########################################################
print(
    "STEP 1. prepare batch of records and common attributes for it (one dimension value and record time)"
)
common_attributes, records = prepare_records()
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records(records=records, common_attributes=common_attributes)
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = all records are written successfully and they all have
# Dimenstion Value: dim_one = 'common_value'
# and the same Record Time
