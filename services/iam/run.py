import os
import json
import boto3
from azure.identity import ClientSecretCredential
from azure.graphrbac import GraphRbacManagementClient

def run(config, logger):
    logger.info(" Starting IAM migration...")

    dry_run = config.get("dry_run", False)

    azure_policies = extract_azure_iam(config, logger)
    logger.info(f" Extracted {len(azure_policies)} Azure IAM policies.")

    transformed_policies = transform_to_aws_format(azure_policies, logger)
    logger.info(" Transformed policies to AWS format.")

    validated_policies = validate_policies(transformed_policies, logger)
    apply_aws_iam(validated_policies, logger, dry_run)
    logger.info(" IAM migration completed.")

# Step 1: Extract Azure IAM policies
def extract_azure_iam(config, logger):
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    client_secret = os.getenv("AZURE_CLIENT_SECRET")

    if not all([tenant_id, client_id, client_secret]):
        logger.error(" Missing Azure credentials.")
        return []

    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    client = GraphRbacManagementClient(credential, tenant_id)

    policies = []
    try:
        for role in client.roles.list():
            permissions = []
            for p in role.permissions:
                permissions.append(p.action)
            policies.append({
                "name": role.name,
                "description": role.description,
                "permissions": permissions
            })
    except Exception as e:
        logger.error(f" Error extracting Azure IAM roles: {e}")
    return policies

# Step 2: Transform to AWS-compatible format
def transform_to_aws_format(policies, logger):
    transformed = []
    for policy in policies:
        aws_policy = {
            "PolicyName": policy["name"].replace(" ", "_"),
            "PolicyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": policy["permissions"],
                        "Resource": "*"
                    }
                ]
            },
            "TrustPolicy": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "ec2.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole"
                    }
                ]
            }
        }
        transformed.append(aws_policy)
    return transformed
# Step 3: validate policies for AWS compatibility
def validate_policies(policies, logger):
    validated = []
    for policy in policies:
        issues = []

        # Check for empty actions
        actions = policy["PolicyDocument"]["Statement"][0].get("Action", [])
        if not actions:
            issues.append("Missing actions")

        # Check for wildcard permissions
        if any(a == "*" or a.endswith(":*") for a in actions):
            issues.append("Overly permissive actions (wildcards)")

        # Check for missing description
        if not policy.get("PolicyName"):
            issues.append("Missing policy name")

        # Check for malformed structure
        if "Version" not in policy["PolicyDocument"] or "Statement" not in policy["PolicyDocument"]:
            issues.append("Malformed policy document")

        if issues:
            logger.warning(f"Policy '{policy.get('PolicyName', 'Unnamed')}' has issues: {', '.join(issues)}")
        else:
            validated.append(policy)

    logger.info(f" {len(validated)} policies passed validation.")
    return validated


# Step 4: Apply policies to AWS
def apply_aws_iam(policies, logger, dry_run=False):
    iam_client = boto3.client("iam")

    for policy in policies:
        policy_name = policy["PolicyName"]
        policy_doc = json.dumps(policy["PolicyDocument"])
        trust_doc = json.dumps(policy["TrustPolicy"])

        if dry_run:
            logger.info(f"[Dry Run] Would create IAM policy: {policy_name}")
            continue

        try:
            # Create IAM policy
            iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=policy_doc
            )
            logger.info(f" Created IAM policy: {policy_name}")
        except iam_client.exceptions.EntityAlreadyExistsException:
            logger.warning(f" Policy already exists: {policy_name}")
        except Exception as e:
            logger.error(f" Failed to create policy {policy_name}: {e}")

        try:
            # Create IAM role with trust policy
            iam_client.create_role(
                RoleName=f"{policy_name}_Role",
                AssumeRolePolicyDocument=trust_doc,
                Description=policy.get("description", "")
            )
            logger.info(f" Created IAM role: {policy_name}_Role")
        except iam_client.exceptions.EntityAlreadyExistsException:
            logger.warning(f" Role already exists: {policy_name}_Role")
        except Exception as e:
            logger.error(f" Failed to create role {policy_name}_Role: {e}")