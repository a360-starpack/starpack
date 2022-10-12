from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep, time
from typing import Optional
import requests
import docker
import shutil

from rich import print
from rich.progress import track

from starpack._config import settings, APP_DIR
from starpack.errors import *


class StarpackClient:

    volume_name: str = "starpack-model-artifacts"
    app_label: str = "starpack-engine"

    def __init__(
        self,
        host: str = "http://localhost",
        port: Optional[int] = 1976,
        start: bool = False,
    ) -> None:

        # Generate the URL based on the provided host and port
        self.host = host
        self.port = port
        self._generate_url()

        if start:
            self._init_docker_client()
            self.start_server()

    def start_server(self):
        """
        Starts the Starpack Engine locally after removing all other instances.
        """
        self.remove_engines()

        # Ensure that we have the Docker Volume to hold saved artifacts and
        # the latest version of our Starpack Engine image from Docker Hub
        self.docker_client.volumes.create(
            name=self.volume_name, labels={"app": self.app_label}
        )
        self.docker_client.images.pull(settings.engine_image)

        print(f"Starting Starpack Engine at {self.url}")
        self.engine = self.docker_client.containers.run(
            image=settings.engine_image,
            name=f"starpack-engine-{round(time())}",
            tty=True,
            ports={80: self.port},
            volumes={
                # Docker-in-Docker mounting
                "/var/run/docker.sock": {
                    "bind": "/var/run/docker.sock",
                    "mode": "rw",
                },
                self.volume_name: {"bind": "/artifacts", "mode": "rw"},
            },
            stdin_open=True,
            detach=True,
            labels={"app": self.app_label},
        )

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

        self._generate_url()

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
                self.engine.put_archive("/artifacts", tar_data)

        print(
            f"Successfully saved {directory} to {directory.name} on the Docker Volume {self.volume_name}"
        )

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

    def remove_engines(self) -> None:
        """
        Finds all instances of starpack engine applications and removes them.
        """
        engines = [
            container
            for container in self.docker_client.containers.list(all=True)
            if ("app", self.app_label) in container.labels.items()
        ]
        if engines:
            for engine in engines:
                engine.remove(force=True)

    def _init_docker_client(self) -> None:
        """
        Initializes a Docker Client
        """
        try:
            self.docker_client = docker.from_env()
        except docker.errors.DockerException:
            raise DockerNotFoundError()

    def _generate_url(self):
        """
        Allows for edge cases if we just have the engine registered with a FQDN
        """
        if self.port is not None:
            self.url = f"{self.host}:{self.port}"
        else:
            self.url = self.host
