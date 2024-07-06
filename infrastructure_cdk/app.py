#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure_cdk.lambda_stack import LambdaStack
from infrastructure_cdk.ecs_stack import ECSStack
from infrastructure_cdk.network_stack import NetworkStack


app = cdk.App()
LambdaStack(app, 
            "Lambda-Stack", 
            env={'region': 'us-west-2'})

NETWORK = NetworkStack(app, 
                       "Network-Stack", 
                       env={'region': 'us-west-2'})


ECSStack(app, 
         "ECS-Stack",
         vpc=NETWORK.vpc,
         env={'region': 'us-west-2'})


app.synth()
