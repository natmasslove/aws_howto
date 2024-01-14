
# Step Function Sample CDK Code - running tasks consecutively and in parallel

see in cdk_test_step_fun\cdk_test_step_fun_stack.py

```python
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
```        