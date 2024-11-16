#!/usr/bin/env python3

import aws_cdk as cdk

from execrole_demo_stack import ExecRoleDemoStack

app = cdk.App()

PROJECT_NAME = "sample"
STAGE_NAME = "all" # resources are shared among all salmon environments 

main_stack = ExecRoleDemoStack(
    app,
    f"cf-{PROJECT_NAME}-ExecRoleDemo-{STAGE_NAME}",
)

app.synth()
