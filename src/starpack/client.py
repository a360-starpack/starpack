from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep, time
from typing import Any, Dict, List, Optional
import requests
import docker
from docker.models.containers import Container
import shutil

from rich import print
from rich.progress import track

from starpack._config import settings, APP_DIR
from starpack.errors import *


class StarpackClient:

    volumes: Dict[str, Dict[str, str]] = {
        "artifacts": {
            "host": "starpack-model-artifacts",
            "container": "/app/external/artifacts",
        },
        "plugins": {
            "host": f"{APP_DIR}/plugins",
            "container": "/app/external/plugins",
        },
    }
    app_label: str = "starpack-engine"

    def __init__(
        self,
        host: str = "http://localhost",
        port: Optional[int] = 1976,
        start: bool = False,
        docker: bool = False,
        force: bool = False,
    ) -> None:

        # Generate the URL based on the provided host and port
        self.host = host
        self.port = port

        if docker:
            self._init_docker_client()

        if start:
            self.start_server(force=force)

    def check_health(self) -> bool:
        """
        Tries to run a healthcheck to see if a server is up.
        """

        try:
            health_response = requests.get(f"{self.url}/healthcheck")
        except requests.ConnectionError:
            return False

        if health_response.status_code != 200:
            return False

        print(f"Successfully connected to server at {self.url}")
        return True

    def package(self, payload: Dict[str, Any]) -> None:
        """
        Packages model artifacts, given a starpack YAML/JSON payload
        """
        package_url = f"{self.url}/package"

        output = requests.post(package_url, json=payload)

        if output.status_code / 100 == 2:
            print(f"Successfully packaged {payload['package']['metadata']['name']}")
        else:
            print(output.status_code)
            print(output.text)

    def remove_engines(self) -> None:
        """
        Finds all instances of starpack engine applications and removes them.
        """
        engines = self._find_engines()
        if engines:
            for engine in engines:
                engine.remove(force=True)

    def start_server(self, force: bool = False):
        """
        Starts the Starpack Engine locally after removing all other instances.
        """
        if force:
            self.remove_engines()
        else:
            engines = self._find_engines()
            if len(engines) == 1:
                # Grab the singular engine if we're not forcing a new start
                self.engine = engines[0]
                if self.engine.status != "running":
                    self.engine.start()
                self.port = self.engine.attrs["HostConfig"]["PortBindings"]["1976/tcp"][
                    0
                ]["HostPort"]
                self._engine_startup_check()
                print(f"Connected to existing engine running at {self.url}")
                return
            elif engines:
                # Case with many engines: Just clean it all out and start again
                self.remove_engines()

        # Ensure that we have the Docker Volume to hold saved artifacts and
        # the latest version of our Starpack Engine image from Docker Hub
        self.docker_client.volumes.create(
            name=self.volumes["artifacts"]["host"], labels={"app": self.app_label}
        )
        self.docker_client.images.pull(settings.engine_image)

        print(f"Starting Starpack Engine at {self.url}")
        self.engine = self.docker_client.containers.run(
            image=settings.engine_image,
            name=f"starpack-engine-{round(time())}",
            tty=True,
            ports={1976: self.port},
            volumes={
                # Docker-in-Docker mounting
                "/var/run/docker.sock": {
                    "bind": "/var/run/docker.sock",
                    "mode": "rw",
                },
                self.volumes["artifacts"]["host"]: {
                    "bind": self.volumes["artifacts"]["container"],
                    "mode": "rw",
                },
                self.volumes["plugins"]["host"]: {
                    "bind": self.volumes["plugins"]["container"],
                    "mode": "rw",
                },
            },
            stdin_open=True,
            detach=True,
            labels={"app": self.app_label},
        )

        self._engine_startup_check()

    def terminate(self, all: bool = False) -> None:
        """
        Terminates a local Docker instance of Starpack Engine and optionally deletes the associated volumes.
        """
        self._init_docker_client()
        self.remove_engines()
        print("Removed all instances of the Starpack Engine")

        if all:
            volume = self.docker_client.volumes.get(self.volume_name)

            volume.remove(force=True)

            print("Removed associated Starpack Engine data")

    def upload_artifacts(self, directory: Path) -> None:
        """
        Given a directory, uploads the contents to our artifacts docker volume.
        """

        directory = directory.resolve()

        # Create a temporary directory to hold our packed up files and create a tarball
        with TemporaryDirectory() as temp_dir:
            dir_archive = shutil.make_archive(
                f"../{directory.name}",
                "tar",
                str(directory.parent),
                str(directory.name),
            )

            with open(dir_archive, "rb") as tar_data:
                self.engine.put_archive(
                    self.volumes["artifacts"]["container"], tar_data
                )

        print(
            f"Successfully saved {directory} to {directory.name} on the Docker Volume {self.volumes['artifacts']['host']}"
        )

    def _find_engines(self) -> List[Container]:
        engines = [
            container
            for container in self.docker_client.containers.list(all=True)
            if ("app", self.app_label) in container.labels.items()
        ]
        return engines

    def _init_docker_client(self) -> None:
        """
        Initializes a Docker Client
        """
        try:
            self.docker_client = docker.from_env()
        except docker.errors.DockerException:
            raise DockerNotFoundError()

    def _engine_startup_check(self) -> None:
        # Check the engine status a few times
        max_attempts = 5
        success = False
        for _ in track(
            range(max_attempts), description="Waiting for the engine to come up..."
        ):
            if not success:
                success = self.check_health()
                sleep(1)

        if not success:
            raise EngineInitializationError()

    @property
    def url(self):
        """
        Allows for edge cases if we just have the engine registered with a FQDN
        """
        if self.port is not None:
            return f"{self.host}:{self.port}"
        else:
            return self.host
