import aws_cdk as core
import aws_cdk.assertions as assertions

from github_actions_cdk.github_actions_cdk_stack import GithubActionsCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in github_actions_cdk/github_actions_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GithubActionsCdkStack(app, "github-actions-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
