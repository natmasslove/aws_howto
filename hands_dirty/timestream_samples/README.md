
# Timestream samples and research

## Description

This short case study provides:
- several code examples on writing records into AWS Timestream tables, getting table properties
- research on write records limitations (limits due to table configutation and, also, AWS service limitations)

## Resources

- /cloudformation - CloudFormation template for Sample Timestream DB, Tables and S3 bucket needed for one of the tables
- /src - Python scripts containing the testing code
- /src/lib/aws - contains a wrapper class over Timestream Boto3 client which you can use in your project :)
- deploy.bat / delete.bat - just contain commands to create/delete CloudFormation stack

## Experiments summary

For more details you can examine python code stored in /src.

### 01. Writing records

Outcome: You can't write more than 100 records in 1 operation (AWS Limit as of time of this test)
Solution: use wrapper class' (in /src/lib/aws) method "write_records" which splits you recordset into 100 record batches and writes those one by one

### 02. Writing records from the past into a table. Part 1.
In Part 1 we use timestream table which has "EnableMagneticStoreWrites" option off (which is default) or can be explicitly stated

```yaml
  TestTable02:
    Type: AWS::Timestream::Table
    Properties:
      DatabaseName: !Ref TestDatabase
      MagneticStoreWriteProperties:
        EnableMagneticStoreWrites: false
```

Also retention settings are applied to the table:
```yaml        
      RetentionProperties: 
        MemoryStoreRetentionPeriodInHours: Y_HOURS
        MagneticStoreRetentionPeriodInDays: Z_DAYS       
```

Outcome: If you want to write a record which has "Time" from X hours ago (inserting event from the past)
- if X <= Y_HOURS (see retention settings) - record is written successfully
- if X > Y_HOURS - record is rejected (if it fits into total Z_DAYS retention interval)
