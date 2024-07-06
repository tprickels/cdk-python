from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_function = _lambda.Function(
            self, 'WelcomeHandler',
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset('lambda-api'),
            handler='welcome.handler'
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_function
        )

        
