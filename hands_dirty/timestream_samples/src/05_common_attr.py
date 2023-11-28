import time
import boto3
import uuid
from lib.aws.timestream_manager import TimestreamTableWriter

# This tests how to insert more than 100 records (uses TimestreamTableWriter batched method to write)

DB_NAME = "timestream-salmon-metrics-events-storage-devam"

ts_client = boto3.client("timestream-write")


def prepare_records():
    records = []

    common_dimensions = [{"Name": "dim_one", "Value": "common_value"}]
    epoch_seconds = time.time()
    record_time = TimestreamTableWriter.epoch_milliseconds_str(
        epoch_seconds=epoch_seconds
    )

    common_attributes = {"Dimensions": common_dimensions, "Time": record_time}

    for i in range(0, 10):
        print(i)
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

table_name = "poc-table-050-common-attr"
writer = TimestreamTableWriter(DB_NAME, table_name, ts_client)

writer.write_records(records=records, common_attributes=common_attributes)
