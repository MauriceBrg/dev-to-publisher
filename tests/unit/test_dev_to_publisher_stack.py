import aws_cdk as core
import aws_cdk.assertions as assertions

from dev_to_publisher.dev_to_publisher_stack import DevToPublisherStack

# example tests. To run these tests, uncomment this file along with the example
# resource in dev_to_publisher/dev_to_publisher_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DevToPublisherStack(app, "dev-to-publisher")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
