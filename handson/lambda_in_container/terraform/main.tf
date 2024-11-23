provider "aws" {
}

# Fetch AWS account ID dynamically
data "aws_caller_identity" "current" {}

# Fetch the current AWS region dynamically
data "aws_region" "current" {}

variable "ecr_repo_name" {
  description = "Name of the ECR repository"
  type        = string
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda-container-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "lambda_execution_policy" {
  name       = "lambda-basic-policy-attachment"
  roles      = [aws_iam_role.lambda_execution_role.name]
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_lambda_function" "lambda_container" {
  function_name = "lambda-container-example"
  role          = aws_iam_role.lambda_execution_role.arn
  package_type  = "Image"

  # Dynamically reference the account ID and region for ECR image URI
  image_uri = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com/${var.ecr_repo_name}:latest"

}
