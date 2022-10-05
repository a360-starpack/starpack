from pathlib import Path
from typing import Optional

import typer

from starpack import app
from starpack import initialize
from starpack.client import StarpackClient


@app.command(name="save")
def save(directory: Path):
    ...


@app.command(name="init")
def initialize_starpack(directory: Optional[Path] = typer.Argument(None)):
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


app()
