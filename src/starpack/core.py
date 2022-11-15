from pathlib import Path
from typing import Optional
from yaml import load, Loader


from starpack import initialize, __version__, utils
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


def init(directory: Optional[Path] = None, force: bool = True) -> StarpackClient:
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


def terminate(
    all_resources: bool = False, client: Optional[StarpackClient] = None
) -> None:
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data
    """

    if not client:
        client = StarpackClient()

    client.terminate(all_resources)


def package(yaml_path: Path, client: Optional[StarpackClient] = None) -> None:
    """
    Takes a YAML file or directory to start the packaging process into a Docker image
    """
    if not yaml_path.exists():
        raise PathExistsError(yaml_path)

    if not client:
        client = StarpackClient(start=True, docker=True)

    input_dict = utils.load_yaml(yaml_path)

    client.package(input_dict)


def package_directory(directory: Path, client: Optional[StarpackClient] = None) -> None:
    """
    Given a directory, uploads the contents, finds the "starpack.yaml", and converts into into a JSON payload for the Starpack Engine to run packaging
    """
    if not directory.is_dir():
        return package(directory)

    yaml_file = directory / "starpack.yaml"

    if not yaml_file.exists():
        raise PathExistsError(yaml_file)

    if not client:
        client = StarpackClient(start=True, docker=True)

    upload(directory, client=client)
    package(yaml_file, client=client)


def deploy(yaml_path: Path, client: Optional[StarpackClient] = None) -> None:
    """
    Takes a YAML file or directory to start the deployment process. If no package exists, also packages the given Starpack artifacts if present in the YAML file.
    """

    if not client:
        client = StarpackClient(start=True, docker=True)

    input_dict = utils.load_yaml(yaml_path)

    client.deploy(input_dict)


def deploy_directory(directory: Path, client: Optional[StarpackClient] = None) -> None:
    """
    Given a directory, uploads the contents, packages, and runs deployment.
    """
    if not directory.is_dir():
        return deploy(directory)

    yaml_file = directory / "starpack.yaml"

    if not yaml_file.exists():
        raise PathExistsError(yaml_file)

    if not client:
        client = StarpackClient(start=True, docker=True)

    package_directory(directory, client=client)
    deploy(yaml_file, client=client)

    return yaml_file
