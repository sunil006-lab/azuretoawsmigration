import os
import uuid
from datetime import datetime

def generate_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def generate_uuid():
    return str(uuid.uuid4())

def file_exists(path):
    return os.path.isfile(path)

def sanitize_dict(d):
    return {k: v for k, v in d.items() if v is not None and v != ""}

def format_tags(tag_dict):
    return [{"Key": k, "Value": v} for k, v in tag_dict.items()]

def validate_required_fields(data, required_keys):
    missing = [key for key in required_keys if key not in data or not data[key]]
    return missing