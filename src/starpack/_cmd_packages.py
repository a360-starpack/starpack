import typer
from pathlib import Path
from typing import Optional

from starpack import package_directory, list_packages, delete_packages

package_app = typer.Typer(pretty_exceptions_show_locals=False)


@package_app.command(name="create")
def cmd_package_create(package_path: Path = typer.Argument(Path("."))) -> None:
    """
    Given a directory, uploads the contents and passes through the contained `starpack.yaml`; given a file, passes as a
    payload as the `yaml` file.
    """
    package_directory(package_path)


@package_app.command(name="delete")
def cmd_package_delete(
        name: str = typer.Option(..., "--name", "-n", help="Name of the package"),
        version: Optional[str] = typer.Option(
            None, "--version", "-v", help="Version of the package"
        ),
        wrapper: Optional[str] = typer.Option(
            None, "--wrapper", "-w", help="Wrapper type of the package"
        ),
) -> None:
    """
    Deletes packages matching the combination of
        - name (required),
        - version (optional)
        - wrapper (optional).
    """
    delete_packages(name, version, wrapper)


@package_app.command(name="list")
def cmd_package_list(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Name of the package"),
        version: Optional[str] = typer.Option(
            None, "--version", "-v", help="Version of the package"
        ),
        wrapper: Optional[str] = typer.Option(
            None, "--wrapper", "-w", help="Wrapper type of the package"
        ),
) -> None:
    """
    Gets details for packages matching the combination of
        - name (required),
        - version (optional)
        - wrapper (optional).
    """
    list_packages(name, version, wrapper)
