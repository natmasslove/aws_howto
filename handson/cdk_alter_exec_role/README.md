
# Altering CDK Execution Role

**Problem Statement**:
By default, the `cdk bootstrap` command in AWS CDK creates a CloudFormation execution role with AdministratorAccess privileges. In certain environments, this level of access is not acceptable. This guide demonstrates workarounds to address this concern.

In this example, we have a CDK Stack which creates only one resource: an SSM Parameter. Therefore, we aim to replace the `AdministratorAccess` policy with a custom policy that grants only SSM-related permissions.

## Creating and Testing CDK with Limited Permissions

### 1. Create a Custom CDK Cloudformation Execution Policy

First, create a custom policy to replace the `AdministratorAccess` policy in the CloudFormation execution role. The policy will only allow SSM-related actions.

Run the following command to deploy the policy:

```bash
aws cloudformation deploy --template-file custom_exec_role_template.yaml --stack-name cd-custom-cdk-exec-role --capabilities CAPABILITY_NAMED_IAM
```

After deployment, note the PolicyArn from the `cd-custom-cdk-exec-role` stack outputs in the CloudFormation console.

### 2. Create CDK Bootstrap with Limited Permissions

Next, bootstrap the CDK environment to use the custom policy:

```bash
cdk bootstrap --cloudformation-execution-policies <<policy_arn>>
```

Replace <<policy_arn>> with the ARN of the policy you created in the previous step.

### 3. Test Stack Deployment

Navigate to the CDK project folder and run:

```bash
cdk deploy
```

## Creating an Isolated CDK Bootstrap with Customized Permissions

In some cases, an existing CDK bootstrap in the same AWS account/region may already be in use, for example, by other projects. To avoid conflicts, you can create an alternative bootstrap distinguished by a different qualifier.

### Prerequisite

Ensure you have created a policy as demonstrated in Step 1 of the previous section.

### 1. Create an Isolated CDK Bootstrap

Run the following command to create a separate bootstrap stack:

```bash
cdk bootstrap --qualifier <<your_qualifier_name>> --cloudformation-execution-policies <<put created policy Arn here>> --toolkit-stack-name <<your_stack_name>>
```

Replace placeholders:

- **your_qualifier_name**: A unique string (up to 10 characters) to identify this bootstrap. It will be used when running CDK commands.
- **your_stack_name**: A custom name for the bootstrap CloudFormation stack. For example, use CDKToolkitMyProject instead of the default CDKToolkit.

### 2. Test Stack Deployment with Custom Qualifier

To use the custom bootstrap during deployment, provide the qualifier via context:

```bash
cdk deploy -c "@aws-cdk/core:bootstrapQualifier=<<your_qualifier_name>>"
```

Replace **your_qualifier_name** with the name of the qualifier you used during the bootstrap process.
