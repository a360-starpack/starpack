import pytest
from typer.testing import CliRunner
from starpack.__main__ import app

@pytest.fixture
def test_runner():
    return CliRunner()

@pytest.mark.parametrize("resource", ("deployment", "model", "package"))
def test_command_list(resource: str, test_runner):
    result = test_runner.invoke(app, ["list", resource])
    assert result.exit_code == 0
    assert resource in result.stdout

    print(result.stdout)
