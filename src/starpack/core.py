from pathlib import Path
from typing import Optional


from starpack import initialize, __version__
from starpack.client import StarpackClient
from starpack.errors import *


def upload(directory: Path, client: Optional[StarpackClient] = None) -> None:
    """
    Uploads the contents of a local directory to the Starpack Engine
    """
    try:
        directory = Path(directory)
    except:
        return

    if not client:
        client = StarpackClient(start=True, docker=True)

    client.upload_artifacts(directory=directory)


def init(
    directory: Optional[Path] = None,
    force: bool = True
) -> StarpackClient:
    """
    Starts the starpack-engine container locally and furthermore initializes
    the given directory if given with starter code, an example
    requirements.txt, and an example starpack.yaml
    """

    StarpackClient(start=True, docker=True, force=force)

    # Create the directory if given
    if directory:
        directory = directory.resolve()
        directory.mkdir(parents=True, exist_ok=True)
        initialize.initialize_project_files(directory)

    return StarpackClient

def terminate(all_resources: bool = False, client: Optional[StarpackClient] = None) -> None:
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data
    """
    
    if not client:
        client = StarpackClient()

    client.terminate(all_resources)


def package(yaml_path: Path):
    """
    Takes a YAML file or directory to start the packaging process into a Docker image
    """
    if not yaml_path.exists():
        raise PathExistsError(yaml_path)
    ...


def package_directory(directory: Path):
    if not directory.is_dir():
        return package(directory)
    ...