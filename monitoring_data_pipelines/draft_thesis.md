
# Monitoring Data Pipelines on AWS

- What are specific features of data pipelines monitoring comparing to "system observability" in general?
- Generally we focus on continuous monitoring of such things as CPU usage and react, e.g. scaling up when CPU utilization goes up.
- For data pipelines we are more focused on discrete things - such as pipeline step completion.

## Goals of monitoring

1. Reactive 
2. Basis for proactive analysis

- Provide a holistic view of all (in most cases, multitude) of pipeline's health

- 

- Identify individual pipeline step completion. Especially when it failed (in some cases we might want to monitor successful completions too)

    - In case of failure we may send a notification message to a relevant person or channels (e.g. Slack, MS Teams), providing as much information as possible
    - Sometimes, you need to make sure data is updated / business-critical report is prepared successfully, again, using some notification methods. If you don't receive the expected message in time - you need to go and check.

- Identify when execution takes longer than expected
    - For daily batch jobs you can understand how long does it take to complete typically

- Keep pipeline execution history (metrics such as execution time, resource consumption as well as error messages)


## Challenges


** Big companies -> 
    there are multiple pipelines
    are developed and managed by multiple teams
    often deployed in different AWS accounts and regions

** Recipient should receive only relevant notifications 

** 


<<Internal capabilities - from MWAA>>    
<<Internal capabilities - from AWS (Cloudwatch, SNS, etc.)>>