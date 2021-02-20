#!/usr/bin/env python3

from aws_cdk import core

from cdk_test.cdk_test_stack import CdkTestStack


app = core.App()
CdkTestStack(app, "cdk-test")

app.synth()
