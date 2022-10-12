from pathlib import Path
from typing import Optional
from rich import print

import typer

from starpack import initialize, __version__, upload, init, terminate
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
def cmd_upload(directory: Path):
    """
    Command to upload the contents of a local directory to the Starpack Engine

    `directory` should be a path that exists on your local host machine.
    """
    upload(directory=directory)


@app.command(name="init")
def cmd_init(
    directory: Optional[Path] = typer.Argument(None),
    force: bool = typer.Option(
        False,
        "--force",
        "-F",
        help="Force a removal of all older starpack-engine containers",
    ),
):
    """
    Starts the starpack-engine container locally and furthermore initializes
    the given directory if given with starter code, an example
    requirements.txt, and an example starpack.yaml
    """

    init(directory=directory, force=force)


@app.command(name="terminate")
def cmd_terminate(
    all_resources: bool = typer.Option(
        False, "--all", "-A", help="Remove associated volumes and saved data as well."
    )
):
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data.
    """

    terminate(all_resources=all_resources)


if __name__ == "__main__":
    app()
