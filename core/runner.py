from services import iam, cicd, s3, lambda_service, rds

SERVICE_REGISTRY = {
    "iam": iam.run,
    "cicd": cicd.run,
    "s3": s3.run,
    "lambda": lambda_service.run,
    "rds": rds.run,
}

def run_services(selected_services, config, logger):
    for service in selected_services:
        service = service.lower().strip()
        if service in SERVICE_REGISTRY:
            try:
                logger.info(f" Starting migration for: {service}")
                SERVICE_REGISTRY[service](config, logger)
                logger.info(f" Completed migration for: {service}")
            except Exception as e:
                logger.error(f" Error during {service} migration: {e}")
        else:
            logger.warning(f" Service '{service}' is not registered in the migration agent.")