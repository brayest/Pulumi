"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3

# Load Parameters
config = pulumi.Config()

# Variables
CompanyName = config.require('CompanyName')
Environment = config.require('Environment')

# Create an AWS resource (S3 Bucket)
backend_bucket = s3.Bucket(
    "{}-s3-backend-{}".format(CompanyName, Environment),
    versioning = {
        'enabled': True
    },
    server_side_encryption_configuration = {
        'rule': {
            'applyServerSideEncryptionByDefault': {
                'sse_algorithm': 'AES256'
            }
        }
    },
    tags = {
        "Environment": Environment,
        "Name": "{}-s3-backend-{}".format(CompanyName, Environment),
    }
)

# Export the name of the bucket
pulumi.export('backend_bucket_name', backend_bucket.id)
