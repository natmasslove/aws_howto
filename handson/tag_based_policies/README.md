
# Tag-based policies demo

This project demonstrates how to create policies allowing access based on tags attached to resources.

Resources in this projects:

1. Two SNS topics (one with tag "project_name" assigned, one - without a tag)
2. Two secrets (one with tag "project_name" assigned, one - without a tag)
3. IAM Role allowing
   1. publish to SNS topic ONLY if the topic has "project_name" tag with certain value
   2. read Secret value (again, ONLY if tag requirements are met)
4. Lambda function which in try-except block tries to publish a message to both SNS topics and read both secrets.

Resulting execution to test out access: SNS publish to topic #1 succeeds, to topic #2 - fails. The same for reading secret values.