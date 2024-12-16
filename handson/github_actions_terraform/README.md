
# Overview

This hands-on section provides a recipe to set up Terraform deployment executions via GitHub Actions.
GitHub actions agent authenticate using OIDC, without storing AWS credentials in repository.

## Create IAM Role (which is used for OIDC authentication when running GitHub Actions)

1. Browse to github_role
2. Run `terraform init`
3. Create terraform.tfvars file to put your values:

```terraform
github_repository = "owner/repo"
project           = "aws_how_to"
stage             = "all"
```

Note: project and stage and used only as a part of role's and policy's name (to abide naming convention).

4. Run `terraform apply`

This creates IAM Role. Please note the IAM Role's arn in outputs.

5. Create secrets in your GitHub repo:
   1. "IAM_ROLE_ARN", put ARN from output as a value.
   2. "AWS_REGION", assign the region where you want github workflows to operate.




