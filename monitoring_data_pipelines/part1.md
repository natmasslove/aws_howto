
# Monitoring Data Pipelines on AWS. Part 1: Specifics, challenges and AWS Toolset

In this two-part article we are going to cover several aspects in regard of monitoring data pipelines running on AWS:
1. How monitoring data pipelines is different from any generic observability tools?
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

In this section let's take a look at AWS Services available for us to build monitoring platform, their typical use-cases, pros and cons.

### Amazon EventBridge