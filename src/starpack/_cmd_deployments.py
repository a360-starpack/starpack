import typer
from pathlib import Path
from typing import Optional

from starpack import deploy_directory, logs, list_deployments, delete_deployments

deployment_app = typer.Typer(pretty_exceptions_show_locals=False)


@deployment_app.command(name="create")
def cmd_deploy_create(deploy_path: Path = typer.Argument(Path("."))) -> None:
    """
    Given a starpack.yaml, deploys a Starpack Package into the environment designated within.
    """
    deploy_directory(deploy_path)


@deployment_app.command(name="delete")
def cmd_deployment_delete(
    name: str = typer.Option(..., "--name", "-n", help="Name of the deployment"),
    version: Optional[str] = typer.Option(
        None, "--version", "-v", help="Version of the deployment"
    ),
    wrapper: Optional[str] = typer.Option(
        None, "--wrapper", "-w", help="Wrapper type of the deployment"
    ),
) -> None:
    """
    Deletes deployments matching the combination of
        - name (required),
        - version (optional)
        - wrapper (optional).
    """
    delete_deployments(name, version, wrapper)


@deployment_app.command(name="logs")
def cmd_deployment_logs(
    name: str = typer.Option(..., "--name", "-n", help="Name of the deployment"),
    version: Optional[str] = typer.Option(
        None, "--version", "-v", help="Version of the deployment"
    ),
    wrapper: Optional[str] = typer.Option(
        None, "--wrapper", "-w", help="Wrapper type of the deployment"
    ),
    output: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output",
        help="Optional output location for the logs to be exported to.",
    ),
) -> None:
    """
    Gets logs for a deployment matching the combination of
        - name (required),
        - version (optional)
        - wrapper (optional).

    Optionally, you can export logs to a given file.
    """
    logs(name, version, wrapper, output)


@deployment_app.command(name="list")
def cmd_deployment_list(
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Name of the deployment"),
    version: Optional[str] = typer.Option(
        None, "--version", "-v", help="Version of the deployment"
    ),
    wrapper: Optional[str] = typer.Option(
        None, "--wrapper", "-w", help="Wrapper type of the deployment"
    ),
) -> None:
    """
    Gets details for deployments matching the combination of
        - name (required),
        - version (optional)
        - wrapper (optional).
    """
    list_deployments(name, version, wrapper)
