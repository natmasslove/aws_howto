#!/usr/bin/env python3

import aws_cdk as cdk

from sample_stack import SampleStack

app = cdk.App()

PROJECT_NAME = "sample"
STAGE_NAME = "all" # resources are shared among all salmon environments 

main_stack = SampleStack(
    app,
    f"cf-{PROJECT_NAME}-SampleStack-{STAGE_NAME}",
)

app.synth()
