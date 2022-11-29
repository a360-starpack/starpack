from pathlib import Path
from string import Template
import shutil
from typing import Dict
from rich import print
from starpack._config import BASE_DIR
from starpack.errors import UserDeclined
import typer


def initialize_project_files(directory: Path, overwrite: bool = False):
    """
    Given a directory to initialize, copies over some starter files.
    """
    template_dir = BASE_DIR / "templates"

    # Copy the simple files
    copy_file(template_dir / "requirements.txt", directory, overwrite=overwrite)
    copy_file(template_dir / "predict.py", directory, overwrite=overwrite)

    # Add the full directory path as a parameter for ease of use
    starpack_yaml_mapping = {"directory": directory.name}
    render_file(
        template_dir / "starpack.yaml",
        directory,
        starpack_yaml_mapping,
        overwrite=overwrite,
    )

    print(f"Completed initializing project directory: {directory}")


def setup_file_output(
    template_file: Path, output_dir: Path, overwrite: bool = False
) -> Path:
    """
    Checks for the existence of the output file and either returns the path or raises an error
    """
    filename = template_file.name
    output_path = output_dir / filename

    if output_path.exists() and not overwrite:
        confirmation = typer.confirm(
            f"{filename} already exists in {output_dir}. Would you like to overwrite it?"
        )
        if not confirmation:
            raise UserDeclined()

    print(f"Creating {output_path}")
    return output_path


def render_file(
    template_file: Path,
    output_dir: Path,
    render_mapping: Dict[str, str],
    overwrite: bool = False,
) -> None:
    """
    Given an input template file and where to render it to, renders according to a render mapping.
    """
    try:
        output_path = setup_file_output(template_file, output_dir, overwrite)
    except UserDeclined:
        return

    output = Template(template_file.read_text()).substitute(render_mapping)
    output_path.write_text(output)


def copy_file(template_file: Path, output_dir: Path, overwrite: bool = False) -> None:
    """
    Copies a template file to a target directory.
    """
    try:
        output_path = setup_file_output(template_file, output_dir, overwrite)
    except UserDeclined:
        return

    shutil.copy(template_file, output_path)
