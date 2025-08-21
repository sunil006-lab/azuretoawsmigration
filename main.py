import argparse
import logging
import yaml
import sys
from core.runner import run_services

def load_config(path):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f" Failed to load config file: {e}")
        sys.exit(1)

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger("MigrationAgent")

def main():
    parser = argparse.ArgumentParser(description=" Azure-to-AWS Migration Agent")
    parser.add_argument('--services', nargs='+', required=True, help='List of services to migrate (e.g., iam cicd s3)')
    parser.add_argument('--config', default='config/default.yaml', help='Path to config file')
    args = parser.parse_args()

    logger = setup_logger()
    config = load_config(args.config)

    if config.get("dry_run"):
        logger.info(" Dry-run mode enabled. No changes will be applied.")

    run_services(args.services, config, logger)

if __name__ == "__main__":
    main()