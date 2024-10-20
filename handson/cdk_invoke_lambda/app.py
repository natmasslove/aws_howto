#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.lambda_invoke_stack import LambdaInvokeStack


app = cdk.App()
LambdaInvokeStack(app, "LambdaInvokeCdkStack")
app.synth()
