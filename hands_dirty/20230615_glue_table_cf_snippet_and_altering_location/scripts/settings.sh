#!/usr/bin/env bash

project_name="athenatbl"
tags="ProjectName=${project_name}"

account_id=$(aws sts get-caller-identity --query "Account" --output text | tr -d '\r')
s3_bucket_name="s3-${project_name}-${account_id}"
echo $s3_bucket_name