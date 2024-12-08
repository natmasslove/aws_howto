
# Example - creating Aurora PostgreSQL serverless V2 cluster

This demo provides an AWS CDK stack to create Aurora PostgreSQL serverless v2 cluster.

It uses L1 constructs which, at the moment of this writing, might provide better control over the process.

Features:

- Master Username / Password are automatically generated (and, then, maintained) by Aurora.
- Scaling: This example demonstrates how to scale cluster down to 0 (no compute charge) during inactivity periods. The official documentation (at the moment of this writing) says the minimum is 0.5 compute units.

