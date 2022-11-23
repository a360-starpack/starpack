from typing import Any, Dict
from yaml import load, Loader
from pathlib import Path


def load_yaml(yaml_path: Path) -> Dict[str, Any]:
    """
    Given a path, load in the YAML as a Python dict
    """
    with open(yaml_path) as yaml_file:
        output_dict = load(yaml_file, Loader)

    return output_dict
