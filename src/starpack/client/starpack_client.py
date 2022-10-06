from time import sleep, time
from typing import Optional
import requests
import docker

from rich import print

from starpack._config import settings
from starpack.errors import *


class StarpackClient:
    def __init__(self, host: str, port: Optional[int] = 1976) -> None:

        self.host = host
        self.port = port
        self._generate_url()

        try:
            self.docker_client = docker.from_env()
        except docker.errors.DockerException:
            raise DockerNotFoundError()

        # Go through all running containers in Docker and find any with the `app`: `starpack-engine` label and grab its port
        engine_ports = [
            container.attrs["HostConfig"]["PortBindings"]["80/tcp"][0]["HostPort"]
            for container in self.docker_client.containers.list()
            if ("app", "starpack-engine") in container.labels.items()
        ]

        if engine_ports:
            self.port = int(engine_ports[0])
            self._generate_url()
            print(f"Found the server running at {self.url}")
        else:
            self.start_server()
            sleep(3)
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
        self.docker_client.images.pull(settings.engine_image)

        print(f"Starting Starpack Engine at {self.url}")
        self.docker_client.containers.run(
            image=settings.engine_image,
            name=f"starpack-engine-{round(time.time())}",
            tty=True,
            ports={80: self.port},
            volumes={
                "/var/run/docker.sock": {
                    "bind": "/var/run/docker.sock",
                    "mode": "rw",
                }
            },
            stdin_open=True,
            detach=True,
            labels={"app": "starpack-engine"},
        )

    def check_health(self):

        try:
            health_response = requests.get(f"{self.url}/healthcheck")
        except requests.ConnectionError:
            raise ValueError("Unable to get response from Starpack Engine.")

        if health_response.status_code != 200:
            raise AttributeError("Starpack Engine is unhealthy!")

        print(f"Successfully connected to server at {self.url}")

    def save_model(self):
        ...
