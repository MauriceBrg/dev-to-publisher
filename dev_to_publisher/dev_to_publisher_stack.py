import os

from aws_cdk import (
    # Duration,
    Stack,
    CfnOutput,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as py_lambda,
)
from constructs import Construct

from local import API_KEY

SRC_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "src"
)

class DevToPublisherStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        publisher = py_lambda.PythonFunction(
            self,
            "publisher",
            entry=SRC_DIR,
            runtime=_lambda.Runtime.PYTHON_3_9,
            index="handler.py",
            handler="lambda_handler",
        )

        api = apigw.RestApi(
            self,
            "rest-api",
            rest_api_name="dev-to-publisher",
            deploy=True,
        )

        api_key = api.add_api_key(
            "honeycode-key",
            api_key_name="honeycode",
            value=API_KEY
        )

        usage_plan = api.add_usage_plan(
            "honeycode",
            api_stages=[
                apigw.UsagePlanPerApiStage(api=api, stage=api.deployment_stage)
            ],
            name="HoneycodeUsagePlan",
        )

        usage_plan.add_api_key(api_key)

        lambda_integration = apigw.LambdaIntegration(
            publisher,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method(
            "POST",
            lambda_integration,
            api_key_required=True,
        )   # POST /
