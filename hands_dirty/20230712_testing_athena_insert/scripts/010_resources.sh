#!/usr/bin/env bash

source settings.sh

################################################################################

file_name="010-resources"
stack_name="cfrm-${project_name}-${file_name}"

  aws cloudformation deploy \
    --template-file ../cloudformation/${file_name}.yaml \
    --stack-name ${stack_name} \
    --no-fail-on-empty-changeset \
    --parameter-overrides ProjectName=${project_name} \
    --tags ${tags} \
    --capabilities CAPABILITY_NAMED_IAM
