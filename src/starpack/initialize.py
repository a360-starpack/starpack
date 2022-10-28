from pathlib import Path
from string import Template
import shutil
from typing import Dict
from rich import print
from starpack._config import BASE_DIR


def initialize_project_files(directory: Path):
    """
    Given a directory to initialize, copies over some starter files.
    """
    template_dir = BASE_DIR / "templates"

    # Copy the simple files
    copy_file(template_dir / "requirements.txt", directory)
    copy_file(template_dir / "predict.py", directory)

    # Add the full directory path as a parameter for ease of use
    starpack_yaml_mapping = {"directory": directory.name}
    render_file(
        template_dir / "package.starpack.yaml", directory, starpack_yaml_mapping
    )

    print(f"Completed initializing project directory: {directory}")


def render_file(
    template_file: Path, output_dir: Path, render_mapping: Dict[str, str]
) -> None:
    """
    Given an input template file and where to render it to, renders according to a render mapping.
    """
    filename = template_file.name
    output_path = output_dir / filename

    print(f"Creating {output_path}")

    output = Template(template_file.read_text()).substitute(render_mapping)
    output_path.write_text(output)


def copy_file(template_file: Path, output_dir: Path) -> None:
    """
    Copies a template file to a target directory.
    """
    filename = template_file.name
    output_path = output_dir / filename

    print(f"Creating {output_path}")

    shutil.copy(template_file, output_path)
