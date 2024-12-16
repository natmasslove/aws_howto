provider "aws" {}

# Input Variables
variable "github_repository" {
  description = "The GitHub repository in the format owner/repo"
  type        = string
}

variable "project" {
  type = string
}

variable "stage" {
  type = string
}

# Data Source to Get AWS Account ID Dynamically
data "aws_caller_identity" "current" {}

# IAM Role
resource "aws_iam_role" "github_oidc_role" {
  name = "role-${var.project}-github-service-role-${var.stage}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" : "sts.amazonaws.com"
          },
          StringLike = {
            "token.actions.githubusercontent.com:sub" : "repo:${var.github_repository}:*"
          }
        }
      }
    ]
  })
}

# IAM Policy for Role Permissions
resource "aws_iam_policy" "ssm_full_access_policy" {
  name        = "policy-${var.project}-github-ssm-${var.stage}"
  description = "Policy granting full SSM access"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "ssm:*",
        Resource = "*"
      }
    ]
  })
}

# Attach Policy to Role
resource "aws_iam_role_policy_attachment" "attach_ssm_policy" {
  role       = aws_iam_role.github_oidc_role.name
  policy_arn = aws_iam_policy.ssm_full_access_policy.arn
}

# Output the Role ARN
output "iam_role_arn" {
  description = "The ARN of the IAM role for GitHub OIDC authentication"
  value       = aws_iam_role.github_oidc_role.arn
}
