
# Monitoring Data Pipelines on AWS. Part 1: Specifics, challenges and AWS Toolset

In this two-part article we are going to cover several aspects in regard of monitoring data pipelines running on AWS:
1. How monitoring data pipelines is different from any general-purpose observability tools?
2. What are typical goals of this kind of observability systems? 
3. What are the common challenges we face when building such system?
4. AWS tools and services useful for this purpose
5. How we've built an open-source monitoring system on top of AWS toolset (to help users addresses monitoring challenges easier and more efficiently)

What we describe here is based on our experience and pain points we heard from our customers.

## How monitoring data pipelines is different from any generic observability tools?

When we think about "typical" monitoring system, the first thing comes to mind is watching over CPU load of EC2 instance or container, and, when needed, reacting to load changes by scaling up or down.  
In a Data Pipelines domain, observations are done on a more "discrete" level. We are focusing more on pipeline steps (if they have completed successfully or fails; did they meet SLA etc.).
It requires a slightly different approach and, as a result, a different toolset.

## Goals of monitoring

1. Make sure all pipelines are running smoothly (with minimal time and efforts required from operation team).
2. Detect failures as soon as possible, get clear notification in case of an error, telling what happened, where and helping to find a root cause. A nice addition would be to keep the history on incidents, so we can perform a retrospective analysis.
3. Detect potential issues. For example, a Glue Job takes longer and longer to complete over time, so there is a risk of breaking SLA in future (e.g. one day it will not complete in time to update the data for downstream reports).
4. Have a graphical, easy-to-grasp representation of current data pipelines' state and execution history. It's preferable to have a centralized place where data about (potentially) numerous pipelines of your organization.

## Challenges

Let's explore some challenges typically encountered when building monitoring solutions in data domain.  
All of them are real-life cases which we solved together with our customers.

1. There are multiple pipelines in scope for monitoring. They belong to different projects and managed/supported by different teams.  
- It's a good idea to introduce a common organization-wide standard (or even ready-to-use solution) which project teams can adopt in their projects instead of reinventing the wheel each time.
- When we introduce a centralized monitoring system, it should be able to distinguish one project from another, so, for example, upon job X failure, alerts should be sent only to a team which manages relevant project.

2. It's not uncommon for organizations to scatter resources among multiple AWS Accounts and regions.  
Here it's important to make sure monitoring data (such as alerts and metrics) are fetched into centralized platform properly.
It involves settings the cross-account relationships, making sure the cross-account permissions are as restrictive as possible and minimizing the footprints of gathering data.

3. Sometimes, technology stack can differ from project to project (e.g. one team chose Glue, another one is relying on EMR stack).
So, centralized platform should be capable of handling events in variety of services.

4. When building a centralized observability platform, we shouldn't require changes in actual pipelines' codebase: we might have some legacy projects in scope (which can be very hard to change), also we cann't rely on multiple teams 100% following coding guidelines.

4. Non-trivial cases, such "detect when something didn't happen". For example, we start the daily processing pipeline when third party uploads a file on S3. So, not getting this file on time can be a reason to notify relevant support team.

## AWS Tools and Services

In this section let's take a look at some AWS Services which can be useful when building the monitoring platform, their typical use-cases, pros and cons.

### Triggering Alerts: Amazon EventBridge
You can set up EventBridge Rules to react on certain AWS events in your account and send those events to a target (where you can process those and send notifications).  
The service provides extensive capabilities for filtering relevant events. For example, you can catch event only from "glue" service with event type "Glue Job State Change" when the target state means "something went wrong".  
Additionally, you can limit the scope of the rule to glue jobs only relevant for your needs (see example below).

```yaml
      EventPattern:
        source:
          - aws.glue
        detail-type:
          - Glue Job State Change
        detail:
          state:
            - FAILED
            - ERROR
            - STOPPED
          jobName:
            - prefix: glue-myproject
```

AWS lets you choose from a variety of services to be a target of this event.  
For our purpose the following seems to be most useful:
- SNS topic - if you just want to send event "as is" to alerts recipients
- SQS queue or Lambda function - if you want to apply additional processing (formatting, beautification for better readility. Maybe enriching the message adding more details).

We found this to be a very nice and efficient way of catching failure. Easy to setup and flexible.

Unfortunately not all services are supported (at time of this writing). For example, you can't catch Glue Workflow or Lambda function failures.
And of course, it takes additional effort to start handling events from another AWS account.

### Catching Lambda Failures: Lambda Destinations

Configuring Lambda Destinations is a great way to get notifications on Lambda failure.
When function fails, it sends an event to the target of your choice (currently available options are SNS, SQS, Lambda and Eventbridge).

![Lambda Destinations Configuration](img/lambda_destinations.png)

There are several downsides:
- it only works when lambda is invoked asynchronously
- it requires Lambda function configuration changes (which, as we discussed in "Challenges" section, not always possible).

### Notifications: AWS SNS vs AWS SES

When monitoring system identifies failure, it's time to send a notification to relevant recipients.

The first candidate service for this is AWS SNS. It's easy to set up and integrates very well with AWS services
(for example, if you set up EventBridge rule (see above), it's a matter of 1 click to set up an SNS Topic as destination).
All topic's subscribers will get the notification. The problem is that notification itself looks like a big chunk of JSON and
desperately lacks readability.

It would be nice to have a formatted message, which outlines the most important aspects of what has happened, making operation team life easier.

One option here is to use the combination of AWS Lambda and SES (which is capable of sending nice HTML e-mails).
You can choose processing Lambda as event target, do some parsing/formatting in Lambda and, then, call SES to deliver the notification.

Generally speaking, when you use processing lambda function as a target, you can send notification in differen ways: to Slack or MS Teams channels etc., but this requires additional efforts for integrations.

### Historical analysis: Cloudwatch LogInsights

AWS services accumulate their logs in CloudWatch and you can use LogInsight tools to query these events in nice, intuitive manner.
For example, that's how you can identify the history of errors of a certain Lambda function:

![CloudWatch LogInsights](img/log_insights.png)

However, for some other services, unlike AWS Lambda, it might require additional coding efforts to store sufficient information about errors (or events in general).

Also, we need to keep in mind, AWS charges based on volume of data (cloudwatch logs) scanned.

### Gathering execution metrics: AWS SDK, AWS CLI

Apart from getting on-failure notification, you might want to collect some execution metrics for future analysis.
For example, you want to gather daily Glue Job running time and DPU-hours consumed.
AWS provides an access to this information over the API, which you can call either using AWS CLI or via AWS SDK.

Here's an example code to extract Glue Job execution time (simplified for demo purposes):
```python
import boto3

def get_glue_job_execution_times(job_name):
    client = boto3.client('glue')

    response = client.get_job_runs(JobName=job_name)
    job_runs = response.get('JobRuns', [])

    execution_times = []

    for run in job_runs:
        execution_time = run.get('ExecutionTime')
        if execution_time: # only for completed runs
            execution_times.append({
                'RunId': run.get('Id'),
                'ExecutionTime': execution_time
            })

    return execution_times

if __name__ == "__main__":
    job_name = 'glue-salmonts-sparkjob-one-dev'
    execution_times = get_glue_job_execution_times(job_name)
    for run in execution_times:
        print(f"RunId: {run['RunId']}, ExecutionTime: {run['ExecutionTime']}")
```





## What's next

In the next part we discuss how we built an open-source solution on top of aforementioned (and other) AWS services to 
meet the goals and address challenges I mentioned in this part.

Stay tuned!
