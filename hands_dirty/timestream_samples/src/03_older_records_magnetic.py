import time
import boto3
import uuid
from lib.aws.timestream_manager import TimestreamTableWriter

# This tests how to insert more old records (older than <x> hours into a table)
# In this script we are experimenting with a table which has 
# EnableMagneticStoreWrites set to True

DB_NAME = "timestream-sample-db"
TABLE_NAME = "poc-table-03-older-records-magnetic"

ts_client = boto3.client('timestream-write')

def prepare_records(hours_old: int):
    records = []

    epoch_seconds = time.time() - hours_old*60*60 # record written successfully

    for i in range(0, 1):
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
print("STEP 0. We get the information about RetentionPeriod settings in the table")
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    hours_retention_memory = writer.get_MemoryStoreRetentionPeriodInHours()
    days_retention_disk = writer.get_MagneticStoreRetentionPeriodInDays()
    print(f"""For the table {TABLE_NAME}: 
MemoryStoreRetentionPeriodInHours = {hours_retention_memory} 
MagneticStoreRetentionPeriodInDays = {days_retention_disk} 
""")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result:
# For the table poc-table-03-older-records-magnetic:
# MemoryStoreRetentionPeriodInHours = 12
# MagneticStoreRetentionPeriodInDays = 5

#########################################################
print("STEP 1. prepare 1 record to insert. Record_time fits in MemoryStoreRetentionPeriodInHours interval")
hours_old = hours_retention_memory - 1 # 1 hour less than MemoryStoreRetentionPeriodInHours
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
hours_old = hours_retention_memory + 1 # 1 hour more than MemoryStoreRetentionPeriodInHours
records = prepare_records(hours_old)
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records_simple(records) 
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = SUCCESS (the record is written directly into magnetic storage layer)

#########################################################
print("STEP 3. prepare 1 record to insert. Record even DOESN'T fit in MagneticStoreRetentionPeriodInDays interval")
hours_old = days_retention_disk * 24 + 1 # 1 hour more than MagneticStoreRetentionPeriodInDays
records = prepare_records(hours_old)
try:
    writer = TimestreamTableWriter(DB_NAME, TABLE_NAME, ts_client)
    writer.write_records_simple(records) 
    print("Written successfully")
except Exception as ex:
    print(f"Error: {str(ex)}")
# Result = SUCCESS (it's still in "kind of" retention range)

#########################################################
print("STEP 4. prepare 1 record to insert. Record by far (more than 1 day) DOESN'T fit in MagneticStoreRetentionPeriodInDays interval")
hours_old = days_retention_disk * 24 + 25 # 25 hour more than MagneticStoreRetentionPeriodInDays
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
# Rejected Index 0: The record timestamp is outside the time range [2023-11-23T06:45:39.648Z, 2023-11-28T19:25:39.648Z) 
# of the data ingestion window.
