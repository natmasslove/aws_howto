
Goal: to test if we can insert data into S3-based CSV / Parquet tables

Results (spoiler :) ):
1. Can't insert into CSV table if there are any non-varchar fields there
2. CSV table #2 (create from CTAS with all columns converted into VARCHAR):
    - Inserts can be performed
    - Initially CTAS statement created .gz file in new table's location
    - Each new insert appends a new .gz file containing added rows
3. Parquet table (even with non-varchar columns):
    - Can handle inserts
    - Initially CTAS statement created a file in new table's location
    - Each new insert appends a new file containing added rows

# Steps to create infrastructure:

1. Run scripts/010_resources.sh - Cloudformation Stack that creates s3 bucket (for sample data)
2. Run scripts/020_copy_datasets.sh - Copies csv file: dataset.cs to S3 bucket
3. Run scripts/020_resources.sh - Cloudformation Stack to create Glue Database and Glue Table in Data Catalog.  

# Testing

## Original table
1. Check table exists and has been populated:

```sql
select * from "sample_table"
```
Result: 10 rows shown

2. Trying to insert data:
```sql
insert into sample_table (id, name, age, version) values (100,'Pete',99,'Ver1')
```
Resulting error:
```text
GENERIC_INTERNAL_ERROR: class org.apache.hadoop.hive.serde2.objectinspector.primitive.WritableIntObjectInspector cannot be cast to class org.apache.hadoop.hive.serde2.objectinspector.primitive.StringObjectInspector (org.apache.hadoop.hive.serde2.objectinspector.primitive.WritableIntObjectInspector and org.apache.hadoop.hive.serde2.objectinspector.primitive.StringObjectInspector are in unnamed module of loader io.trino.server.PluginClassLoader @13809190). 
```

## Varchar-only CSV table
1. Create a new table from initial one (converting column types - required):
```sql
CREATE table sample_table_from_ctas
WITH (format='CSV',
external_location = 's3://s3-athenatestins-658207859208/csv_table_from_ctas/')
AS
SELECT cast(id as varchar) as id, name, cast(age as varchar) as age, version
FROM sample_table
LIMIT 5
```

[Link to AWS Doc](https://docs.aws.amazon.com/athena/latest/ug/ctas.html)

Result: .gz file is created in csv_table_from_ctas/ folder (I believe, compression type can be changed via options given in SQL statement).  
Selecting from table - works well.

2. Insert one row into the table:
```sql
INSERT INTO sample_table_from_ctas (id, name, age, version)
SELECT cast(id as varchar) as id, name, cast(age as varchar) as age, version
  FROM sample_table
 WHERE id = 7 
```

Result: One more .gz file created in table's S3 subfolder

Note: INSERT INTO .. VALUES .. syntax also works well as long as all values are strings.

```sql
INSERT INTO sample_table_from_ctas (id, name, age, version)
VALUES ('100','Pete','99','ver')
```

3. Update and delete commands fail (expectedly :) ) with an error:

```sql
update  sample_table_from_ctas set age = '35' where id = '100';

delete from sample_table_from_ctas where id = '100';
```

```text
NOT_SUPPORTED: Modifying Hive table rows is only supported for transactional tables
```

## Parquet table
1. Create a new Parquet table from initial csv one:

```sql
CREATE table parquet_table_from_ctas
WITH (format='PARQUET',
parquet_compression='SNAPPY',
external_location = 's3://s3-athenatestins-658207859208/parquet_table_from_ctas/')
AS
SELECT id, name, age, version
FROM sample_table
LIMIT 5
```

Result:
- Table is created
- One file in table's s3 subfolder (no file extension, but by options it should be snappy.parquet)

2. Insert
```sql
INSERT INTO parquet_table_from_ctas (id, name, age, version)
SELECT id, name, age, version
  FROM sample_table
 WHERE id = 7 
```

Result:
- Row is inserted
- One additional file created in S3 subfolder

3. Update and delete commands fail (expectedly :) ) with an error:

```sql
update  parquet_table_from_ctas set age = 35 where id = 100;

delete from parquet_table_from_ctas where id = 100;
```

```text
NOT_SUPPORTED: Modifying Hive table rows is only supported for transactional tables
```

## Iceberg table
1. Create an Iceberg Parquet table from initial csv one:

```sql
CREATE table iceberg_table_from_ctas
WITH (format='PARQUET', table_type='ICEBERG', is_external = false,
location = 's3://s3-athenatestins-658207859208/iceberg_table_from_ctas/')
AS
SELECT id, name, age, version
FROM sample_table
LIMIT 5
```

Result:
- Table created
- S3 location contains two subfolders /data, /metadata

2. Insert
```sql
INSERT INTO iceberg_table_from_ctas (id, name, age, version)
SELECT id, name, age, version
  FROM sample_table
 WHERE id = 7 
```

Result:
- Row is inserted
- Additional files created in S3 subfolders for data and metadata

3. Update and delete commands fail (expectedly :) ) with an error:

```sql
update  iceberg_table_from_ctas set age = 35 where id = 7;

delete from iceberg_table_from_ctas where id = 7;
```

Result:
- Row updated and deleted successfully
- Additional files created in S3 subfolders for data and metadata