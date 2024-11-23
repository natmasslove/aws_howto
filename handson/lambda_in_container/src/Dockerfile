FROM public.ecr.aws/lambda/python:3.13

# Copy function code
COPY app.py .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]