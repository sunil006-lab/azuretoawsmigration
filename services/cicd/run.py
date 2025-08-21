import os
import json
import boto3
import yaml

def run(config, logger):
    logger.info(" Starting CI/CD pipeline migration...")

    dry_run = config.get("dry_run", False)
    azure_pipeline_path = config.get("azure_pipeline_path", "data/azure_pipeline.yaml")

    azure_pipeline = extract_azure_pipeline(azure_pipeline_path, logger)
    transformed_pipeline = transform_to_aws_pipeline(azure_pipeline, logger)
    validated_pipeline = validate_pipeline(transformed_pipeline, logger)

    deploy_aws_pipeline(validated_pipeline, logger, dry_run)

# Step 1: Extract Azure DevOps pipeline YAML
def extract_azure_pipeline(path, logger):
    try:
        with open(path, 'r') as f:
            pipeline = yaml.safe_load(f)
            logger.info(f" Loaded Azure pipeline from {path}")
            return pipeline
    except Exception as e:
        logger.error(f" Failed to load Azure pipeline: {e}")
        return {}

# Step 2: Transform to AWS CodePipeline format
def transform_to_aws_pipeline(azure_pipeline, logger):
    stages = []
    for step in azure_pipeline.get("steps", []):
        stages.append({
            "name": step.get("task", "Unnamed"),
            "action": "Build",
            "provider": "CodeBuild",
            "configuration": {
                "commands": step.get("script", "")
            }
        })

    aws_pipeline = {
        "name": "MigratedPipeline",
        "roleArn": "arn:aws:iam::123456789012:role/CodePipelineServiceRole",
        "artifactStore": {
            "type": "S3",
            "location": "your-artifact-bucket"
        },
        "stages": stages
    }

    logger.info(" Transformed Azure pipeline to AWS format.")
    return aws_pipeline

# Step 3: Validate pipeline structure
def validate_pipeline(pipeline, logger):
    issues = []

    if not pipeline.get("name"):
        issues.append("Missing pipeline name")
    if not pipeline.get("stages"):
        issues.append("No stages defined")
    if not pipeline.get("artifactStore", {}).get("location"):
        issues.append("Missing artifact store location")

    if issues:
        logger.warning(f" Pipeline validation issues: {', '.join(issues)}")
    else:
        logger.info(" Pipeline passed validation checks.")

    return pipeline

# Step 4: Deploy to AWS CodePipeline
def deploy_aws_pipeline(pipeline, logger, dry_run=False):
    if dry_run:
        logger.info(f"[Dry Run] Would deploy pipeline: {pipeline['name']}")
        return

    client = boto3.client("codepipeline")

    try:
        response = client.create_pipeline(pipeline=pipeline)
        logger.info(f" Deployed AWS CodePipeline: {pipeline['name']}")
    except client.exceptions.PipelineNameInUseException:
        logger.warning(f" Pipeline already exists: {pipeline['name']}")
    except Exception as e:
        logger.error(f" Failed to deploy pipeline: {e}")