#!/usr/bin/env bash

script_folder=$(dirname "${BASH_SOURCE[0]}")

source ${script_folder}/../settings.sh

###################################################################
# 1. delete bucket (it contains files, so CF deletion will fail)

aws s3 rb s3://$s3_bucket_name --force

###################################################################

stack_name="cfrm-${project_name}-030-athena"

  aws cloudformation delete-stack --stack-name ${stack_name}

  echo "Waiting for stack ${stack_name} to be deleted..."

  aws cloudformation wait stack-delete-complete --stack-name ${stack_name}

# ###################################################################

stack_name="cfrm-${project_name}-010-resources"

  aws cloudformation delete-stack --stack-name ${stack_name}

  echo "Waiting for stack ${stack_name} to be deleted..."

  aws cloudformation wait stack-delete-complete --stack-name ${stack_name}

