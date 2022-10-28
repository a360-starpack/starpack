from pathlib import Path
import pytest
from typer.testing import CliRunner
import docker

from starpack.__main__ import app
from starpack.client import StarpackClient


class FakeContainer:
    labels = {
        "desktop.docker.io/wsl-distro": "Ubuntu-20.04",
        "app": "starpack-engine",
    }
    attrs = {
        "HostConfig": {
            "PortBindings": {"1976/tcp": [{"HostIp": "", "HostPort": "1976"}]},
        }
    }

    status = "running"

    def remove(*args, **kwargs):
        ...


class FakeContainerModule:
    def list(*args, **kwargs):
        return [FakeContainer]

    def run(*args, **kwargs):
        pass


class FakeImageModule:
    def pull(*args):
        pass


class FakeVolume:
    def remove(*args, **kwargs):
        ...


class FakeVolumesModule:
    def get(*args, **kwargs):
        return FakeVolume()

    def create(*args, **kwargs):
        ...


class FakeDockerClient:
    def __init__(self, *args, **kwargs) -> None:
        self.containers = FakeContainerModule
        self.images = FakeImageModule
        self.volumes = FakeVolumesModule


@pytest.fixture(autouse=True)
def mock_docker(monkeypatch, requests_mock):
    monkeypatch.setattr(docker, "from_env", FakeDockerClient)
    requests_mock.get(
        "http://localhost:1976/healthcheck", text='{"healthy": "true"}', status_code=200
    )


@pytest.fixture
def test_runner(monkeypatch):
    return CliRunner()


def test_command_init(tmp_path: Path, test_runner: CliRunner):
    result = test_runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0
    assert "Completed initializing project directory:" in result.stdout


def test_command_version(test_runner: CliRunner):
    result = test_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Starpack CLI version" in result.stdout
