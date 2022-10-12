from pathlib import Path
from typing import Optional
from rich import print

import typer

from starpack import initialize, __version__
from starpack.client import StarpackClient

app = typer.Typer(pretty_exceptions_show_locals=False)


def version_callback(give_version: bool) -> None:
    if give_version:
        print(f"Starpack CLI version: {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True
    )
):
    return


@app.command(name="upload")
def upload(directory: Path):
    """
    Uploads the contents of a local directory to the Starpack Engine
    """
    client = StarpackClient()

    client.upload_artifacts(directory=directory)


@app.command(name="init")
def initialize_starpack(
    directory: Optional[Path] = typer.Argument(None),
    local: bool = typer.Option(True, "--local", "-l"),
):
    """
    Starts the starpack-engine container locally and furthermore initializes
    the given directory if given with starter code, an example
    requirements.txt, and an example starpack.yaml
    """

    StarpackClient(start=True)

    # Create the directory if given
    if directory:
        directory = directory.resolve()
        directory.mkdir(parents=True, exist_ok=True)
        initialize.initialize_project_files(directory)


@app.command(name="terminate")
def terminate_starpack(
    all: bool = typer.Option(
        False, "--all", "-A", help="Remove associated volumes and saved data as well."
    )
):
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data.
    """

    client = StarpackClient()

    client.terminate(all)


if __name__ == "__main__":
    app()
