import time
import boto3
import uuid
from lib.aws.timestream_manager import TimestreamTableWriter

# This tests how to insert more old records (older than <x> hours for memory storage of a table)
# Provided that table has magnetic storage option on

DB_NAME = "timestream-salmon-metrics-events-storage-devam"

ts_client = boto3.client('timestream-write')

def prepare_records():
    records = []

    # table settings:
    #   RetentionProperties: 
    #     MemoryStoreRetentionPeriodInHours: 24
    #     MagneticStoreRetentionPeriodInDays: 10

    # Results in
    # 1. time fits in memory storage interval -> SUCCESS
    # hours = 23
   
    # 2. time fits in magnetic storage interval, but not in memory interval -> SUCCESS
    # hours = 48

    # 3. time doesn't fits in magnetic storage interval -> FAILURE: No error, but records simply doesn't show up
    hours = 24 * 10 + 24
    
    epoch_seconds = time.time() - hours*60*60 # record rejected

    for i in range(0, 1):
        print(i)
        dimensions = [
            {
                "Name": "dim_one",
                "Value": f"hrs: -{hours}",
            },
            {
                "Name": "dim_two",
                "Value": str(uuid.uuid1()),
            }
        ]
        
        record_time = TimestreamTableWriter.epoch_milliseconds_str(epoch_seconds = epoch_seconds)

        records.append(
            {
                "Dimensions": dimensions,
                "MeasureName": "measure_1",
                "MeasureValue": str(i),
                "MeasureValueType": "BIGINT",
                "Time": record_time,
            }
        )

    return records


records = prepare_records()

table_name = "poc-table-3-magnetic"
writer = TimestreamTableWriter(DB_NAME, table_name, ts_client)

writer.write_records(records)
