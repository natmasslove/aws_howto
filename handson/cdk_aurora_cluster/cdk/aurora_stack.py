from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_secretsmanager as secretsmanager,
    custom_resources as cr,
)
from constructs import Construct

DB_ENGINE = "aurora-postgresql"
DB_ENGINE_MODE = "provisioned"
DB_ENGINE_VERSION = "16.4"
DEFAULT_DB_NAME = "pocdb"


class AuroraStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Get default VPC
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # Security Group
        db_security_group = ec2.SecurityGroup(
            self,
            "DBSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
            description="Security group for Aurora DB",
        )
        db_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(5432), "Allow from anyone on port 5432"
        )

        # Subnet Group
        db_subnet_group = rds.CfnDBSubnetGroup(
            self,
            "DBSubnetGroup",
            db_subnet_group_name="subnetgrp-aurora-sample",
            subnet_ids=[subnet.subnet_id for subnet in vpc.public_subnets],
            db_subnet_group_description="Subnet group for Aurora DB",
        )

        # Aurora Cluster
        db_cluster = rds.CfnDBCluster(
            self,
            "DBCluster",
            engine=DB_ENGINE,
            engine_mode=DB_ENGINE_MODE,
            engine_version=DB_ENGINE_VERSION,
            db_cluster_identifier="salmon-poc",
            database_name=DEFAULT_DB_NAME,
            manage_master_user_password=True,  # AWS creates a secret containing master user credentials
            master_username="postgres",
            port=5432,
            db_subnet_group_name=db_subnet_group.ref,
            vpc_security_group_ids=[db_security_group.security_group_id],
            serverless_v2_scaling_configuration={
                "minCapacity": 0,  # contradicts the documentation (it says min = 0.5), but now Aurora allows 0 for certain cluster types
                "maxCapacity": 2,
            },
            deletion_protection=False,
            enable_http_endpoint=True,
        )

        # Aurora Instance
        rds.CfnDBInstance(
            self,
            "DBInstance",
            db_instance_identifier="poc-main-instance",
            db_instance_class="db.serverless",
            engine=DB_ENGINE,
            engine_version=DB_ENGINE_VERSION,
            db_cluster_identifier=db_cluster.ref,
            publicly_accessible=True,
            db_subnet_group_name=db_subnet_group.ref,
        )

        # Outputs
        CfnOutput(
            self,
            "ClusterEndpoint",
            value=db_cluster.attr_endpoint_address,
            description="The endpoint to connect to the Aurora cluster.",
        )
        CfnOutput(
            self,
            "ClusterPort",
            value=db_cluster.attr_endpoint_port,
        )
        CfnOutput(
            self,
            "ClusterDBName",
            value=DEFAULT_DB_NAME,
        )
        CfnOutput(
            self,
            "ClusterMasterSecretARN",
            value=db_cluster.attr_master_user_secret_secret_arn,
        )
