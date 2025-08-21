import os
import yaml

def load_yaml_config(path, logger=None):
    if not os.path.isfile(path):
        if logger:
            logger.error(f" Config file not found: {path}")
        return {}

    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
            if logger:
                logger.info(f" Loaded config: {path}")
            return config or {}
    except yaml.YAMLError as e:
        if logger:
            logger.error(f" YAML parsing error in {path}: {e}")
        return {}
    except Exception as e:
        if logger:
            logger.error(f" Failed to load config {path}: {e}")
        return {}