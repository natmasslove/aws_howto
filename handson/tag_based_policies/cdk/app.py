#!/usr/bin/env python3
import sys

import aws_cdk as cdk


from tag_based_access_stack import TagBasedAccessStack

app = cdk.App()

PROJECT_NAME = "testam"
STAGE_NAME = "all" # resources are shared among all salmon environments 

main_stack = TagBasedAccessStack(
    app,
    f"cf-{PROJECT_NAME}-TagBasedAccessStack-{STAGE_NAME}",
)

app.synth()
