from pathlib import Path
from typing import Optional

from starpack import initialize, __version__, utils
from starpack.client import StarpackClient
from starpack.errors import *


def upload(
    directory: Path, client: Optional[StarpackClient] = None
) -> None:
    """
    Uploads the contents of a local directory to the Starpack Engine
    """

    client.upload_artifacts(directory=directory)


def initialize_directory(directory: Path, overwrite: bool = False) -> None:
    """
    Starts the starpack-engine container locally and furthermore initializes
    the given directory if given with starter code, an example
    requirements.txt, and an example starpack.yaml
    """
    if directory:
        directory = directory.resolve()
        directory.mkdir(parents=True, exist_ok=True)
        initialize.initialize_project_files(directory, overwrite=overwrite)


def initialize_engine(force: bool = True) -> StarpackClient:
    """
    Starts the Starpack Engine. If given an image name, will initialize that image. If given
    """
    client = StarpackClient(start=True, docker=True, force=force)

    return client


def terminate(
    all_resources: bool = False, client: StarpackClient = StarpackClient()
) -> None:
    """
    Terminates and removes the Starpack Engine container and optionally removes all associated data
    """

    if not client:
        client = StarpackClient()

    client.terminate(all_resources)


def package(
    yaml_path: Path, client: Optional[StarpackClient] = None
) -> None:
    """
    Takes a YAML file or directory to start the packaging process into a Docker image
    """
    if not yaml_path.exists():
        raise PathExistsError(yaml_path)

    if not client:
        client = StarpackClient(start=True, docker=True)

    input_dict = utils.load_yaml(yaml_path)

    client.package(input_dict)


def package_directory(
    directory: Path, client: Optional[StarpackClient] = None
) -> None:
    """
    Given a directory, uploads the contents, finds the "starpack.yaml", and converts into a JSON payload for the Starpack Engine to run packaging
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


def deploy(
    yaml_path: Path, client: Optional[StarpackClient] = None,
) -> None:
    """
    Takes a YAML file or directory to start the deployment process. If no package exists, also packages the given Starpack artifacts if present in the YAML file.
    """

    if not client:
        client = StarpackClient(start=True, docker=True)

    input_dict = utils.load_yaml(yaml_path)

    client.deploy(input_dict)


def deploy_directory(
    directory: Path, client: Optional[StarpackClient] = None
) -> None:
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


def list_deployments(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client: Optional[StarpackClient] = None,
) -> None:
    """
    Lists deployments matching the combination of name (required), version (optional), and wrapper (optional).
    """
    if not client:
        client = StarpackClient(start=True, docker=True)

    print(client.list_deployments(name, version, wrapper))


def list_packages(
    name: Optional[str] = None,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client: Optional[StarpackClient] = None,
) -> None:
    """
    Lists deployments matching the combination of name (required), version (optional), and wrapper (optional).
    """
    if not client:
        client = StarpackClient(start=True, docker=True)

    print(client.list_packages(name, version, wrapper))


def delete_deployments(
    name: str,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client: Optional[StarpackClient] = None,
) -> None:
    """
    Deletes deployments matching the combination of name (required), version (optional), and wrapper (optional).
    """
    if not client:
        client = StarpackClient(start=True, docker=True)

    client.delete_deployments(name, version, wrapper)


def delete_packages(
    name: str,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    client: Optional[StarpackClient] = None,
) -> None:
    """
    Deletes packages matching the combination of name (required), version (optional), and wrapper (optional).
    """
    if not client:
        client = StarpackClient(start=True, docker=True)

    client.delete_packages(name, version, wrapper)


def logs(
    name: str,
    version: Optional[str] = None,
    wrapper: Optional[str] = None,
    output: Optional[Path] = None,
    client: Optional[StarpackClient] = None,
) -> None:
    """
    Deletes deployments matching the combination of name (required), version (optional), and wrapper (optional).
    """
    if not client:
        client = StarpackClient(start=True, docker=True)

    log_text = client.get_logs(name, version, wrapper)

    if output:
        output.write_text(log_text)
        print(f"Wrote logs to {output.resolve()}")
    else:
        print(output)

