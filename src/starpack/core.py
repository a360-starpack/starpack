from pathlib import Path
from typing import Optional


from starpack import initialize, __version__
from starpack.client import StarpackClient


def upload(directory: Path):
    """
    Uploads the contents of a local directory to the Starpack Engine
    """
    try:
        directory = Path(directory)
    except:
        return
    client = StarpackClient(start=True, docker=True)

    client.upload_artifacts(directory=directory)


def init(
    directory: Optional[Path] = None,
    force: bool = False,
):
    """
    Starts the starpack-engine container locally and furthermore initializes
    the given directory if given with starter code, an example
    requirements.txt, and an example starpack.yaml
    """

    StarpackClient(start=True, docker=True, force=True)

    # Create the directory if given
    if directory:
        directory = directory.resolve()
        directory.mkdir(parents=True, exist_ok=True)
        initialize.initialize_project_files(directory)


def terminate(all_resources: bool = False):
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data.
    """

    client = StarpackClient()

    client.terminate(all_resources)
