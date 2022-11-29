import pytest
from pathlib import Path
from starpack import errors


def test_docker_not_found_error() -> None:
    with pytest.raises(errors.DockerNotFoundError) as e:
        raise errors.DockerNotFoundError()

    assert e.value.exit_code == 1


def test_local_only_error() -> None:
    with pytest.raises(errors.LocalOnlyError) as e:
        raise errors.LocalOnlyError()

    assert e.value.exit_code == 1


def test_path_exists_error(capsys) -> None:
    with pytest.raises(errors.PathExistsError) as e:
        path = Path()
        raise errors.PathExistsError(path)

    output = capsys.readouterr()

    assert str(path) in output.out
    assert e.value.exit_code == 1


def test_engine_initialization_error() -> None:
    with pytest.raises(errors.EngineInitializationError) as e:
        raise errors.EngineInitializationError()

    assert e.value.exit_code == 1
