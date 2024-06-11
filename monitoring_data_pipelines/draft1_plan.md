

Monitoring Data Pipelines. Part 1: Goals, Challenges and AWS Toolset

* Intro 
  ++ in this 2-parts article I'd like to tell you about .. successful experience of building a tool which started as
   .. an internal project, but emerged to a full open-source project.


* Specifics of monitoring data pipelines
* What do I, as an end-user, want from Data Pipeline Observability Tools
  * be notified on important events (not only failures, but successful execution for important report)
  * notifications should let me easily identify what happened
  * to do some retrospective analysis
  * create reports & dashboard -> minimize time spent on monitoring activities
  * detect unexpected behavior (not only failures, but prolonged execution time)

  * ++Feel free to add comments if you have other cases
* Common challenges
  * Multiple regions and AWS accounts
  * Independent teams manage one project or another



* AWS Toolset
  * EventBridge + SNS - ex. on Glue Job failure
  * AWS CLI or SDK - "aws glue get-job-runs"
  * CloudWatch Metrics and alarms
  


Monitoring Data Pipelines. Part 2: Building on top of AWS Capabilities


  Note: some tools (like Airflow) can have their own notifications and if all your projects are similar - use that tool.
  On the other hand, 1) if your want to have single point  2) if your tools doesn't have advanced capabilities
  (advanced - beautiful notification)