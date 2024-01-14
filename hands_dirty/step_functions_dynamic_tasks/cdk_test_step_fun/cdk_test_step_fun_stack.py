from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as sfn_tasks,    
)
from constructs import Construct

MIN_ID = 0
MAX_ID = 10000

class CdkTestStepFunStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_iam_roles()

        lambda_function = self.create_lambda_functions(lambda_role)

        sm = self.create_step_function_consecutive(lambda_function)       
        sm = self.create_step_function_consecutive_dynamic(lambda_function)       
        sm = self.create_step_function_parallel(lambda_function)       


    def create_iam_roles(self):

        # IAM Role for Lambda
        lambda_role = iam.Role(
            self, "LambdaRole",
            role_name='role-stepfuntest-1',
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )

        return lambda_role

    def create_lambda_functions(self, lambda_iam_role: iam.Role):
        pass

        current_region = Stack.of(self).region
        #powertools_layer = get_lambda_powertools_layer(self, current_region)

        lambda_path = "source/"

        # get_titled_players_lambda
        test_lambda = lambda_.Function(
            self,
            "TestLambda",
            function_name="lambda-teststepfun",
            code=lambda_.Code.from_asset(
                lambda_path
            ),
            handler="lambda_test.lambda_handler",
            timeout=Duration.seconds(900),
            runtime=lambda_.Runtime.PYTHON_3_11,
            role=lambda_iam_role,
            #layers=[powertools_layer],
            retry_attempts=2,
            #on_failure=lambda_destiantions.SnsDestination(internal_error_topic),
        )    

        return test_lambda
    
    def create_step_function_consecutive(self, lambda_function: lambda_.Function):                
        submit_job = sfn_tasks.LambdaInvoke(
            self, "Submit Job",
            lambda_function=lambda_function,
            payload=sfn.TaskInput.from_object({"message" : "Hello"}),
            output_path="$.Payload",
        )

        submit_job2 = sfn_tasks.LambdaInvoke(
            self, "Submit Job 2",
            lambda_function=lambda_function,
            payload=sfn.TaskInput.from_object({"message" : "Second Hello"}),
            output_path="$.Payload",
        )        

        chain = submit_job.next(submit_job2)

        # Create state machine
        sm = sfn.StateMachine(
            self, "StateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(chain),
        )

        return sm        
    
    def create_step_function_consecutive_dynamic(self, lambda_function: lambda_.Function):                

        chain = None
        for i in range(1,5):
            submit_job = sfn_tasks.LambdaInvoke(
                self, f"SubmitJobConsecDyn{i}",
                lambda_function=lambda_function,
                payload=sfn.TaskInput.from_object({"message" : f"Hello{i}"}),
                output_path="$.Payload",
            )
            if chain is None:
                chain = submit_job
            else:
                chain = chain.next(submit_job)

        # Create state machine
        sm = sfn.StateMachine(
            self, "StateMachineConsecDynamic",
            definition_body=sfn.DefinitionBody.from_chainable(chain),
        )

        return sm         

    def create_step_function_parallel(self, lambda_function: lambda_.Function):                

        parallel = sfn.Parallel(self, "All jobs")
        for i in range(1,5):
            submit_job = sfn_tasks.LambdaInvoke(
                self, f"SubmitJobParallelDyn{i}",
                lambda_function=lambda_function,
                payload=sfn.TaskInput.from_object({"message" : f"Hello{i}"}),
                output_path="$.Payload",
            )

            parallel = parallel.branch(submit_job)

        # Create state machine
        sm = sfn.StateMachine(
            self, "StateMachineParallelDynamic",
            definition_body=sfn.DefinitionBody.from_chainable(parallel),
        )

        return sm            