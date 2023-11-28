import time
import boto3
import uuid
from lib.aws.timestream_manager import TimestreamTableWriter

# This tests how to insert more old records (older than <x> hours into a table)
# In this script we are experimenting with a table which has 
# EnableMagneticStoreWrites: false
# (which is a default option or you can switch it off explicitly)
# p.s.: the next script (03) is for a table allowing magnetic writes

DB_NAME = "timestream-sample-db"
TABLE_NAME = "poc-table-02-older-records-memonly"

ts_client = boto3.client('timestream-write')

def prepare_records(hours_old: int):
    records = []

    epoch_seconds = time.time() - hours_old*60*60 # record written successfully

    for i in range(0, 1):
        print(i)
        dimensions = [
            {
                "Name": "dim_one",
                "Value": "value_one",
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


#########################################################
print("STEP 0. We get the information about MemoryStoreRetentionPeriodInHours settings in the table")
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    hours_retention = writer.get_MemoryStoreRetentionPeriodInHours()
    print(f"For the table {TABLE_NAME}, MemoryStoreRetentionPeriodInHours = {hours_retention}")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = "For the table poc-table-02-older-records-memonly, MemoryStoreRetentionPeriodInHours = 12"   

#########################################################
print("STEP 1. prepare 1 record to insert. Record_time fits in MemoryStoreRetentionPeriodInHours interval")
hours_old = hours_retention - 1 # 1 hour less than MemoryStoreRetentionPeriodInHours
records = prepare_records(hours_old)
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records_simple(records) 
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = SUCCESS   

#########################################################
print("STEP 2. prepare 1 record to insert. Record_time DOESN'T fit in MemoryStoreRetentionPeriodInHours interval")
hours_old = hours_retention + 1 # 1 hour more than MemoryStoreRetentionPeriodInHours
records = prepare_records(hours_old)
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records_simple(records) 
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = Error (record is rejected)
# RejectedRecords:  An error occurred (RejectedRecordsException) when calling the WriteRecords operation: 
# One or more records have been rejected. See RejectedRecords for details.
# Rejected Index 0: The record timestamp is outside the time range [2023-11-28T06:12:10.452Z, 2023-11-28T18:52:10.452Z) 
# of the memory store.



