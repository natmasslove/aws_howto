#!/usr/bin/env python3

import aws_cdk as cdk
import os

from aurora_stack import AuroraStack

app = cdk.App()

PROJECT_NAME = "sample"
STAGE_NAME = "all"  # resources are shared among all salmon environments

main_stack = AuroraStack(
    app,
    f"cf-{PROJECT_NAME}-AuroraStack-{STAGE_NAME}",
    env={
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
        "region": os.environ["CDK_DEFAULT_REGION"],
    },
)

app.synth()
