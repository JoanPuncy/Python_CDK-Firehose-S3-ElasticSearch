from aws_cdk import (
    core,
    aws_elasticsearch as es
)


class CdkElasticSearchStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dev_domain = es.Domain(self, "QueueingDomain", 
        version = es.ElasticsearchVersion.V7_9, 
        enable_version_upgrade = True
        )

        self.elasticSearch = es.CfnDomain(self, "CDKElasticSearch",
            domain_name = "cdk-elasticsearch",
            elasticsearch_version = "7.4",
            access_policies = {
                "Version": "2012-10-17",
                "Statement": [
                    {"Effect": "Allow", 
                    "Principal": {"AWS": ["*"]},
                    "Action": ["es:*"],
                    "Resource": "arn:aws:es:us-east-1:755723993001:domain/cdk-test/*"
                    }
                ]
            },
            elasticsearch_cluster_config = es.CfnDomain.ElasticsearchClusterConfigProperty(
                instance_count           = 1,
                instance_type            = "t3.small.elasticsearch",
                zone_awareness_enabled   = False
            ),
            ebs_options = es.CfnDomain.EBSOptionsProperty(
                ebs_enabled = True,
                iops        = 0,
                volume_size = 20,
                volume_type = "gp2"
            ),
            snapshot_options = es.CfnDomain.SnapshotOptionsProperty (
                automated_snapshot_start_hour = 0
            )
        )