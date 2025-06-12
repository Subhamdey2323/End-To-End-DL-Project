import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from box import ConfigBox
from pathlib import Path
from typing import Any, Dict
import base64
from typing import get_type_hints


def enforce_annotations(func):
    """Decorator to enforce type annotations manually."""
    def wrapper(*args, **kwargs):
        hints = get_type_hints(func)
        for arg_name, arg_value in zip(func.__code__.co_varnames, args):
            expected_type = hints.get(arg_name)
            if expected_type and not isinstance(arg_value, expected_type):
                raise TypeError(f"Argument '{arg_name}' must be of type {expected_type}, got {type(arg_value)}")
        return func(*args, **kwargs)
    return wrapper

@enforce_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads YAML file and returns ConfigBox."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if not content or not isinstance(content, dict):  # Ensure valid mapping
                raise ValueError("YAML file contains invalid data or is empty")
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty or incorrectly formatted")
    except Exception as e:
        raise e

@enforce_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates directories if they don’t exist."""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")

@enforce_annotations
def save_json(path: Path, data: Dict):
    """Saves dictionary data into a JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON file saved at: {path}")
@enforce_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads a JSON file's data and returns a ConfigBox instance."""
    with open(path) as f:
        content = json.load(f)
    logger.info(f"JSON file loaded successfully from: {path}")
    return ConfigBox(content)
@enforce_annotations
def save_bin(data: Any, path: Path):
    """Saves data as a binary file."""
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")
@enforce_annotations
def load_bin(path: Path) -> Any:
    """Loads binary data from a file."""
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data
@enforce_annotations
def get_size(path: Path) -> str:
    """Returns file size in KB."""
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


@enforce_annotations
def decodeImage(imgstring: str, fileName: str):
    """Decodes a Base64 image and writes to a file."""
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)

@enforce_annotations
def encodeImageIntoBase64(croppedImagePath: str) -> bytes:
    """Encodes an image into Base64 format."""
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())
