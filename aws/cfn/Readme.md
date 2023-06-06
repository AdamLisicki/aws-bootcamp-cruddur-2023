## Architecture Guide

Before you tun any templates, be sure to create an S3 bucket to contain
all of our artifacts for CloudFormation.

```
aws s3 mk s3://cfn-artifacts-cruddur
export CFN_BUCKET="cfn-artifacts-cruddur"
gp env CFN_BUCKET="cfn-artifacts-cruddur"
```