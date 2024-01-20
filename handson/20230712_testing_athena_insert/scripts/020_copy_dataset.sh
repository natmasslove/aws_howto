#!/usr/bin/env bash

source settings.sh

################################################################################

aws s3 cp ../datasets/dataset.csv s3://$s3_bucket_name/csv_table/
