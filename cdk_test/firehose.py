from aws_cdk import (
    core,
    aws_kinesisfirehose as firehose,
    aws_s3 as s3,
    aws_iam as iam
)

class CdkFirehoseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Bucket
        bucket = s3.Bucket(self, "cdk-firehose-bucket")

        # IAM Role for Firehose
        firehose_role = iam.Role(self, "FirehoseRole",
            assumed_by = iam.ServicePrincipal(
                service = "firehose.amazonaws.com"
            )
        )

        delivery_policy = iam.Policy(
            self, "FirehosePolicy",
            policy_name = "FirehosePolicy",
            statements = [
                iam.PolicyStatement(
                    effect = iam.Effect.ALLOW,
                    actions = [
                        "s3:AbortMultipartUpload",
                        "s3:GetBucketLocation",
                        "s3:GetObject",
                        "s3:ListBucket",
                        "s3:ListBucketMultipartUploads",
                        "s3:PutObject"
                    ],
                    resources = [
                        bucket.bucket_arn,
                        bucket.bucket_arn+"/*"
                    ]
                )
            ]               
        )

        delivery_policy.attach_to_role(firehose_role)

        # Firehose stream
        delivery_stream = firehose.CfnDeliveryStream(
            self, "QueueingStream",
            delivery_stream_name = "QueueingStream",
            s3_destination_configuration = {
                "bucketArn": bucket.bucket_arn,
                "roleArn": firehose_role.role_arn
            },
            elasticsearch_destination_configuration = None
        )

        # delivery_stream.add_depends_on(firehose_role)

        # We assign the stream's arn and name to a local variable for the Object.
        self._delivery_stream_name = delivery_stream.delivery_stream_name
        self._delivery_stream_arn = delivery_stream.attr_arn
    
    # Using the property decorator to export value delivery_arn
    @property
    def main_delivery_stream_props(self):
        return self._delivery_stream_name, self._delivery_stream_arn