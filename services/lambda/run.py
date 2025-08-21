import os
import json
import boto3
import yaml

def run(config, logger):
    logger.info(" Starting Lambda service migration...")

    dry_run = config.get("dry_run", False)
    lambda_config_path = config.get("lambda_config_path", "data/lambda_config.yaml")

    lambda_definitions = extract_lambda_configs(lambda_config_path, logger)
    transformed_functions = transform_lambda_configs(lambda_definitions, logger)
    validated_functions = validate_lambda_configs(transformed_functions, logger)

    deploy_lambda_functions(validated_functions, logger, dry_run)

# Step 1: Extract Lambda config from YAML
def extract_lambda_configs(path, logger):
    try:
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
            logger.info(f" Loaded Lambda config from {path}")
            return config_data.get("functions", [])
    except Exception as e:
        logger.error(f" Failed to load Lambda config: {e}")
        return []

# Step 2: Transform to AWS-compatible format
def transform_lambda_configs(functions, logger):
    transformed = []
    for fn in functions:
        transformed.append({
            "FunctionName": fn.get("name"),
            "Runtime": fn.get("runtime", "python3.9"),
            "Role": fn.get("role_arn"),
            "Handler": fn.get("handler", "lambda_function.lambda_handler"),
            "Code": {
                "ZipFile": open(fn.get("artifact_path", "dist/lambda.zip"), "rb").read()
            },
            "Description": fn.get("description", ""),
            "Timeout": fn.get("timeout", 10),
            "MemorySize": fn.get("memory", 128),
            "Publish": True
        })
    logger.info(" Transformed Lambda configs to AWS format.")
    return transformed

# Step 3: Validate Lambda configs
def validate_lambda_configs(functions, logger):
    validated = []
    for fn in functions:
        issues = []

        if not fn.get("FunctionName"):
            issues.append("Missing function name")
        if not fn.get("Role"):
            issues.append("Missing IAM role ARN")
        if not fn.get("Handler"):
            issues.append("Missing handler")
        if not fn.get("Runtime"):
            issues.append("Missing runtime")
        if not fn.get("Code"):
            issues.append("Missing code artifact")

        if issues:
            logger.warning(f" Lambda '{fn.get('FunctionName', 'Unnamed')}' has issues: {', '.join(issues)}")
        else:
            validated.append(fn)

    logger.info(f" {len(validated)} Lambda functions passed validation.")
    return validated

# Step 4: Deploy Lambda functions
def deploy_lambda_functions(functions, logger, dry_run=False):
    client = boto3.client("lambda")

    for fn in functions:
        name = fn["FunctionName"]

        if dry_run:
            logger.info(f"[Dry Run] Would deploy Lambda function: {name}")
            continue

        try:
            client.create_function(**fn)
            logger.info(f" Created Lambda function: {name}")
        except client.exceptions.ResourceConflictException:
            logger.warning(f" Function already exists: {name}")
            try:
                update_payload = {
                    "FunctionName": name,
                    "ZipFile": fn["Code"]["ZipFile"]
                }
                client.update_function_code(**update_payload)
                logger.info(f" Updated code for existing Lambda: {name}")
            except Exception as e:
                logger.error(f" Failed to update Lambda code: {e}")
        except Exception as e:
            logger.error(f" Failed to create Lambda function {name}: {e}")