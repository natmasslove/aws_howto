#!/usr/bin/env bash

source settings.sh

################################################################################

aws s3 cp ../datasets/dataset_a.csv s3://$s3_bucket_name/sample/dataset_a/
aws s3 cp ../datasets/dataset_b.csv s3://$s3_bucket_name/sample/dataset_b/