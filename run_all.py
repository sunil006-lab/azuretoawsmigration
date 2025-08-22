
from utils.config_loader import load_yaml_config
from services.iam.run import run as run_iam
from services.s3.run import run as run_s3
from services.lambda.run import run as run_lambda
from services.rds.run import run as run_rds
from services.cicd.run import run as run_cicd
import logging

# Setup logger
logging.basicConfig(filename='logs/migration_agent.log', level=logging.INFO)
logger = logging.getLogger("migration_agent")

# Load default config
config = load_yaml_config("config/default.yaml", logger)

# Run modules
run_iam(config, logger)
run_s3(config, logger)
run_lambda(config, logger)
run_rds(config, logger)
run_cicd(config, logger)