import os
import boto3
from utils.config_loader import load_yaml_config

def run(config, logger):
    logger.info(" Starting RDS migration...")

    dry_run = config.get("dry_run", False)
    rds_config_path = config.get("rds_config_path", "config/rds_config.yaml")

    rds_definitions = load_yaml_config(rds_config_path, logger).get("instances", [])
    transformed_instances = transform_rds_configs(rds_definitions, logger)
    validated_instances = validate_rds_configs(transformed_instances, logger)

    deploy_rds_instances(validated_instances, logger, dry_run)

# Step 1: Transform to AWS-compatible format
def transform_rds_configs(instances, logger):
    transformed = []
    for db in instances:
        transformed.append({
            "DBInstanceIdentifier": db["name"],
            "AllocatedStorage": db.get("storage", 20),
            "DBInstanceClass": db.get("instance_class", "db.t3.micro"),
            "Engine": db["engine"],
            "MasterUsername": db["username"],
            "MasterUserPassword": db["password"],
            "BackupRetentionPeriod": db.get("backup_retention", 7),
            "MultiAZ": db.get("multi_az", False),
            "PubliclyAccessible": db.get("public", False),
            "StorageType": db.get("storage_type", "gp2"),
            "VpcSecurityGroupIds": db.get("security_groups", []),
            "DBSubnetGroupName": db.get("subnet_group", ""),
            "Tags": [{"Key": k, "Value": v} for k, v in db.get("tags", {}).items()]
        })
    logger.info(" Transformed RDS configs to AWS format.")
    return transformed

# Step 2: Validate RDS configs
def validate_rds_configs(instances, logger):
    validated = []
    for db in instances:
        issues = []

        if not db.get("DBInstanceIdentifier"):
            issues.append("Missing DB instance name")
        if not db.get("Engine"):
            issues.append("Missing database engine")
        if not db.get("MasterUsername") or not db.get("MasterUserPassword"):
            issues.append("Missing master credentials")
        if db.get("AllocatedStorage", 0) < 20:
            issues.append("Storage must be at least 20 GB")

        if issues:
            logger.warning(f" RDS '{db.get('DBInstanceIdentifier', 'Unnamed')}' has issues: {', '.join(issues)}")
        else:
            validated.append(db)

    logger.info(f" {len(validated)} RDS instances passed validation.")
    return validated

# Step 3: Deploy RDS instances
def deploy_rds_instances(instances, logger, dry_run=False):
    client = boto3.client("rds")

    for db in instances:
        name = db["DBInstanceIdentifier"]

        if dry_run:
            logger.info(f"[Dry Run] Would create RDS instance: {name}")
            continue

        try:
            client.create_db_instance(**db)
            logger.info(f" Created RDS instance: {name}")
        except client.exceptions.DBInstanceAlreadyExistsFault:
            logger.warning(f" RDS instance already exists: {name}")
        except Exception as e:
            logger.error(f" Failed to create RDS instance {name}: {e}")