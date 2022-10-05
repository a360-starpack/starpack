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
            "PortBindings": {"80/tcp": [{"HostIp": "", "HostPort": "1976"}]},
        }
    }


class FakeContainerModule:
    def list(*args):
        return [FakeContainer]

    def run(*args, **kwargs):
        pass


class FakeImageModule:
    def pull(*args):
        pass


class FakeDockerClient:
    def __init__(self, *args, **kwargs) -> None:
        self.containers = FakeContainerModule
        self.images = FakeImageModule


@pytest.fixture(autouse=True)
def mock_docker(monkeypatch, requests_mock):
    monkeypatch.setattr(docker, "from_env", FakeDockerClient)
    requests_mock.get(
        "http://localhost:1976/healthcheck", text='{"healthy": "true"}', status_code=200
    )


@pytest.fixture
def test_runner(monkeypatch):
    return CliRunner()


def test_command_list(tmp_path: Path, test_runner: CliRunner):
    result = test_runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0
    assert "Completed initializing project directory:" in result.stdout
