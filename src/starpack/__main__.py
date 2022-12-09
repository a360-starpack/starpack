from pathlib import Path
from rich import print
from rich.pretty import pprint

import typer

from starpack import (
    __version__,
    upload,
    initialize_directory,
    initialize_engine,
    terminate,
    package_directory,
    deploy_directory,
)
from starpack._config import settings

app = typer.Typer(pretty_exceptions_show_locals=False)

engine_app = typer.Typer(pretty_exceptions_show_locals=False)

app.add_typer(
    engine_app,
    name="engine",
    help="Commands to control and manipulate the Starpack Engine itself.",
)

# Config app for changing config

config_app = typer.Typer(pretty_exceptions_show_locals=False)

app.add_typer(
    config_app,
    name="config",
    help="View the current Starpack Configuration. You can edit this configuration manually at ~/.starpack/",
    hidden=True,
)


@config_app.command(name="view")
def cmd_view_config():
    """
    View a pretty-printed version of the config, found
    """
    pprint(settings, expand_all=True)


@engine_app.command(name="start")
def cmd_start_engine(
    force: bool = typer.Option(
        False,
        "--force",
        "-F",
        help="Force a removal of all older starpack-engine containers",
    )
):
    """
    Starts the Starpack Engine. If given a custom Docker image name, will attempt to run it instead.
    If `force` is passed, will remove any existing containers and ensure that the latest version is pulled.
    """

    initialize_engine(force=force)


@engine_app.command(name="terminate")
def cmd_engine_terminate(
    all_resources: bool = typer.Option(
        False, "--all", "-A", help="Remove associated volumes and saved data as well."
    )
) -> None:
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data.
    """

    terminate(all_resources=all_resources)


def version_callback(give_version: bool) -> None:
    """
    Returns the current version of Starpack
    """
    if give_version:
        print(f"Starpack CLI version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Returns current version of Starpack CLI",
    )
) -> None:
    return


@app.command(name="upload")
def cmd_upload(directory: Path = typer.Argument(Path("."))) -> None:
    """
    Command to upload the contents of a local directory to the Starpack Engine

    `directory` should be a path that exists on your local host machine.
    """
    upload(directory=directory)


@app.command(name="init")
def cmd_init(
    directory: Path = typer.Argument(Path(".")),
    overwrite: bool = typer.Option(
        False, "--overwrite", "-o", help="Overwrite files without further user input"
    ),
) -> None:
    """
    Initializes the given directory with starter code, an example
    requirements.txt, and an example starpack.yaml
    """

    initialize_directory(
        directory=directory,
        overwrite=overwrite,
    )


@app.command(name="package")
def cmd_package(package_path: Path = typer.Argument(Path("."))) -> None:
    """
    Given a directory, uploads the contents and passes through the contained `starpack.yaml`; given a file, passes as a
    payload as the `yaml` file.
    """
    package_directory(package_path)


@app.command(name="deploy")
def cmd_deploy(deploy_path: Path = typer.Argument(Path("."))) -> None:
    """
    Given a starpack.yaml, deploys a Starpack Package into the environment designated within.
    """
    deploy_directory(deploy_path)


if __name__ == "__main__":
    app()
