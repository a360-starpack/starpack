from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep, time
from typing import Optional
import requests
import docker
import shutil

from rich import print

from starpack._config import settings, APP_DIR
from starpack.errors import *


class StarpackClient:

    volume_name: str = "starpack-model-artifacts"
    app_label: str = "starpack-engine"

    def __init__(self, host: str, port: Optional[int] = 1976) -> None:

        self.host = host
        self.port = port
        self._generate_url()

        try:
            self.docker_client = docker.from_env()
        except docker.errors.DockerException:
            raise DockerNotFoundError()

        # Go through all running containers in Docker and find any with the `app`: `starpack-engine`
        # label and grab its port
        engines = [
            container
            for container in self.docker_client.containers.list(all=True)
            if ("app", self.app_label) in container.labels.items()
        ]

        if not engines:
            self.start_server()
        else:
            # Just keep a single engine and kill all of the others.
            self.engine = engines.pop()
            # self.engine.restart()
            for engine in engines:
                engine.remove(force=True)

        if self.engine.status != "running":
            print("Waiting for engine to come online...")
            self.engine.start()
            sleep(3)
        # Sleep for a bit to allow the server to come up
        # sleep(3)

        self.port = self.engine.attrs["HostConfig"]["PortBindings"]["80/tcp"][0][
            "HostPort"
        ]
        self._generate_url()
        print(f"Found the server running at {self.url}")

        # Ensures that the client is actually up and running.
        self.check_health()

    def _generate_url(self):
        """
        Allows for edge cases if we just have the engine registered with a FQDN
        """
        if self.port:
            self.url = f"{self.host}:{self.port}"
        else:
            self.url = self.host

    def start_server(self):

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

    def check_health(self):

        try:
            health_response = requests.get(f"{self.url}/healthcheck")
        except requests.ConnectionError:
            raise ValueError("Unable to get response from Starpack Engine.")

        if health_response.status_code != 200:
            raise AttributeError("Starpack Engine is unhealthy!")

        print(f"Successfully connected to server at {self.url}")

    def save_artifacts(self, directory: Path) -> None:

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
