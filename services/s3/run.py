import os
import boto3
from utils.config_loader import load_yaml_config

def run(config, logger):
    logger.info(" Starting S3 migration...")

    dry_run = config.get("dry_run", False)
    s3_config_path = config.get("s3_config_path", "config/s3_config.yaml")

    s3_definitions = load_yaml_config(s3_config_path, logger).get("buckets", [])
    transformed_buckets = transform_s3_configs(s3_definitions, logger)
    validated_buckets = validate_s3_configs(transformed_buckets, logger)

    deploy_s3_buckets(validated_buckets, logger, dry_run)

# Step 1: Transform to AWS-compatible format
def transform_s3_configs(buckets, logger):
    transformed = []
    for bucket in buckets:
        transformed.append({
            "Bucket": bucket["name"],
            "ACL": bucket.get("acl", "private"),
            "CreateBucketConfiguration": {
                "LocationConstraint": bucket.get("region", "ap-south-1")
            },
            "Tags": [{"Key": k, "Value": v} for k, v in bucket.get("tags", {}).items()],
            "Objects": bucket.get("objects", [])
        })
    logger.info(" Transformed S3 configs to AWS format.")
    return transformed

# Step 2: Validate bucket configs
def validate_s3_configs(buckets, logger):
    validated = []
    for bucket in buckets:
        issues = []

        if not bucket.get("Bucket"):
            issues.append("Missing bucket name")
        if not bucket.get("CreateBucketConfiguration", {}).get("LocationConstraint"):
            issues.append("Missing region")
        for obj in bucket.get("Objects", []):
            if not os.path.exists(obj.get("source", "")):
                issues.append(f"Missing object source file: {obj.get('source')}")

        if issues:
            logger.warning(f" S3 bucket '{bucket.get('Bucket', 'Unnamed')}' has issues: {', '.join(issues)}")
        else:
            validated.append(bucket)

    logger.info(f" {len(validated)} S3 buckets passed validation.")
    return validated

# Step 3: Deploy buckets and upload objects
def deploy_s3_buckets(buckets, logger, dry_run=False):
    client = boto3.client("s3")

    for bucket in buckets:
        name = bucket["Bucket"]

        if dry_run:
            logger.info(f"[Dry Run] Would create S3 bucket: {name}")
            continue

        try:
            client.create_bucket(
                Bucket=name,
                ACL=bucket["ACL"],
                CreateBucketConfiguration=bucket["CreateBucketConfiguration"]
            )
            logger.info(f" Created S3 bucket: {name}")
        except client.exceptions.BucketAlreadyOwnedByYou:
            logger.warning(f" Bucket already exists: {name}")
        except Exception as e:
            logger.error(f" Failed to create bucket {name}: {e}")
            continue

        # Upload objects
        for obj in bucket.get("Objects", []):
            try:
                client.upload_file(
                    Filename=obj["source"],
                    Bucket=name,
                    Key=obj["key"]
                )
                logger.info(f" Uploaded object '{obj['key']}' to bucket '{name}'")
            except Exception as e:
                logger.error(f" Failed to upload object '{obj['key']}' to bucket '{name}': {e}")