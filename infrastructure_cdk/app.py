#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure_cdk.lambda_stack import LambdaStack


app = cdk.App()
LambdaStack(app, 
            "Lambda-Stack", 
            env={'region': 'us-west-2'})

app.synth()
