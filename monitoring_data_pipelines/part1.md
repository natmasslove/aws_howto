
# Monitoring Data Pipelines on AWS. Part 1: Specifics, challenges and AWS Toolset

In this two-part article we are going to cover several aspects in regard of monitoring data pipelines running on AWS:
1. How monitoring data pipelines is different from any generic observability tools?
2. What are typical goals of this kind of observability systems?
3. AWS tools and services useful for this purpose
4. How we've built an open-source monitoring system on top of AWS toolset (to help users addresses monitoring challenges easier and more efficiently)

What we describe here is based on our experience and pain points we heard from our customers.

## How monitoring data pipelines is different from any generic observability tools?

When we think about "typical" monitoring system, the first thing comes to mind is watching over CPU load of EC2 instance or container, and, when needed, reacting to load changes by scaling up or down.  
In a Data Pipelines domain, observations are done on a more "discrete" level. We are focusing more on pipeline steps (if they have completed successfully or fails; did they meet SLA etc.).
It requires a slightly different approach and, as a result, a different toolset.

## Goals of monitoring

1. Make sure all pipelines are running smoothly (with minimal time and efforts required from operation team).
2. Detect failures as soon as possible, get clear notification in case of an error, telling what happened, where and helping to find a root cause. A nice addition would be to keep the history on incidents, so we can perform retrospective analysis.
3. Detect potential issues. For example
