from typing import Any, Dict
from yaml import load, Loader
from pathlib import Path

def load_yaml(yaml_path: Path) -> Dict[str, Any]:
    with open(yaml_path) as yaml_file:
        output_dict = load(yaml_file, Loader)
    
    return output_dict
    