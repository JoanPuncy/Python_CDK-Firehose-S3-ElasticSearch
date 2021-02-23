#!/usr/bin/env python3
import os 
from aws_cdk import core

from cdk_test.cdk_test_stack import CdkTestStack
from cdk_test.firehose import CdkFirehoseStack
from cdk_test.elasticsearch import CdkElasticSearchStack


env_USA = core.Environment(account="755723993001", region="us-east-1")


app = core.App()
CdkTestStack(app, "cdk-test", env=env_USA)
CdkFirehoseStack(app, "cdk-firehose")
CdkElasticSearchStack(app, "cdk-elasticsearch")

app.synth()
