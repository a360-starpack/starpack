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

    def put_archive(*args, **kwargs):
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
    """Tests `starpack init $PATH`"""
    result = test_runner.invoke(app, ["init", str(tmp_path)])
    assert result.exit_code == 0
    assert "Completed initializing project directory:" in result.stdout


def test_command_init_overwrite(tmp_path: Path, test_runner: CliRunner):
    """Tests `starpack init $PATH` with duplicate files"""
    _ = test_runner.invoke(app, ["init", str(tmp_path)])
    result = test_runner.invoke(app, ["init", str(tmp_path)], "y\nn\ny\n")
    assert result.exit_code == 0
    assert "Completed initializing project directory:" in result.stdout
    assert "predict.py already exists" in result.stdout


def test_command_version(test_runner: CliRunner):
    result = test_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Starpack CLI version" in result.stdout


def test_command_engine_start(test_runner: CliRunner):
    result = test_runner.invoke(app, ["engine", "start"])
    assert result.exit_code == 0


def test_command_upload(tmp_path: Path, test_runner: CliRunner):
    result = test_runner.invoke(app, ["upload", str(tmp_path)])
    assert result.exit_code == 0


def test_command_terminate(test_runner: CliRunner):

    result = test_runner.invoke(app, ["engine", "terminate"])

    assert result.exit_code == 0


fake_payload = """
package:
  metadata:
    # Set the package name to use later for the deployment
    name:  &package_name starpack_test
    description: "Testing package"
    version: 0.0.1
    author: Andromeda 360, Inc.
    author_email: irvin.shen@andromeda360.com
  artifacts:
    root_location: starpack_test
    validation_data:
    training_data:
    inference:
      function_name: predict
      script_name: predict.py
      model_data: pred_heart_disease.pkl
    dependencies: requirements.txt
  steps:
    - name: fastapi
      version: 1.0.0
    - name: docker_desktop_push
      labels:
      image_name: "irvin-killed-it" # optional, defaults to metadata name
      image_tags: # optional
        - latest

deployment:
  metadata:
    name: final_test
    version: 1.0.0
  steps:
  - name: local_docker_find
    version: 1.0.0
    image:
      name: *package_name
      tag: latest
  - name: local_docker_deploy
    version: 1.0.0
    port: # optional
"""


# @pytest.mark.parametrize()
def test_command_package(test_runner: CliRunner, tmp_path, monkeypatch, requests_mock):
    url = "http://localhost:1976/package"
    requests_mock.post(url, status_code=200, text="")

    yaml_path = tmp_path / "starpack.yaml"
    yaml_path.write_text(fake_payload)

    monkeypatch.setattr(StarpackClient, "package", lambda x, y: ...)
    result = test_runner.invoke(app, ["package", str(tmp_path)])

    assert result.exit_code == 0


def test_command_deploy(test_runner: CliRunner, tmp_path, monkeypatch, requests_mock):
    requests_mock.post("http://localhost:1976/deploy", status_code=200, text="")
    requests_mock.post("http://localhost:1976/package", status_code=200, text="")

    yaml_path = tmp_path / "starpack.yaml"
    yaml_path.write_text(fake_payload)

    monkeypatch.setattr(StarpackClient, "deploy", lambda x, y: ...)
    result = test_runner.invoke(app, ["deploy", str(tmp_path)])

    assert result.exit_code == 0
