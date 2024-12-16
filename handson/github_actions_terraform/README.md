
# Terraform Deployment via GitHub Actions with OIDC Authentication

This hands-on guide demonstrates how to set up Terraform deployments using GitHub Actions. The GitHub Actions runner authenticates with AWS using OpenID Connect (OIDC), eliminating the need to store AWS credentials in the repository.

## Step 1: Create an IAM Role for OIDC Authentication

1. Navigate to the IAM Role Terraform Configuration
Browse to the `github_role` folder in your project.

2. Initialize Terraform
Run the following command to initialize Terraform in the directory:

```bash
terraform init
```

3. Create a terraform.tfvars File
Define the required variables in terraform.tfvars to customize the IAM role creation. Example:

```hcl
github_repository = "owner/repo"
project           = "aws_how_to"
stage             = "all"
```

Note: The project and stage variables are only used to follow naming conventions for the role and policy.

4. Apply the Terraform Configuration
Run the following command to create the IAM role:

```bash
terraform apply
```

5. Note the IAM Role ARN and Create Secrets in Your GitHub Repository

After the Terraform run completes, the IAM Role ARN will be displayed in the outputs.

Add the following secrets to your repository for use in workflows:

- `IAM_ROLE_ARN`: Add the ARN of the IAM role created (from terraform output).
- `AWS_REGION`: Specify the AWS region where the Terraform workflows will operate (e.g., us-east-1).


## Step 2: Use the Demo GitHub Workflow for Terraform Deployments

This repository includes a demo GitHub Actions workflow that demonstrates how to deploy infrastructure using Terraform. The workflow references the `main.tf` file in `resources` folder and runs Terraform commands to validate and plan the configuration.

The demo workflow file is located at `.github/workflows/terraform-deploy.yml` and includes the following steps:

- code checkout
- configure AWS credentials
- install Terraform using hashicorp/setup-terraform action
- running `terraform init` and `terraform plan` commands.

### Notes:

- The provided workflow is for demonstration purposes and does **not** include a terraform apply step.
- If you want to enable the terraform apply step, you must configure Terraform state storage (e.g., using an S3 backend) in your main.tf file. This ensures state consistency across runs.

