import time
import boto3
import uuid
import json
from lib.aws.timestream_manager import TimestreamTableWriter

# This tests how to insert more old records (older than <x> hours for memory storage of a table)

DB_NAME = "timestream-salmon-metrics-events-storage-devam"

ts_client = boto3.client('timestream-write')


table_name = "poc-table-040"
writer = TimestreamTableWriter(DB_NAME, table_name, ts_client)



ret_prop = writer.get_MemoryStoreRetentionPeriodInHours()




print(ret_prop)


