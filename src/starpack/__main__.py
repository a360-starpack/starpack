from pathlib import Path
from typing import Optional
from rich import print

import typer

from starpack import app, initialize, __version__
from starpack.client import StarpackClient


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


@app.command(name="save")
def save(directory: Path):
    ...


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

    StarpackClient("http://localhost", 1976)

    # Create the directory if given
    if directory:
        directory = directory.resolve()
        directory.mkdir(parents=True, exist_ok=True)
        initialize.initialize_project_files(directory)


if __name__ == "__main__":
    app()
