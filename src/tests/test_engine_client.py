from starpack.client import StarpackClient
import requests
import pytest
from typing import Optional


@pytest.fixture
def starpack_client():
    client = StarpackClient()

    return client


def test_client_initialization():
    client = StarpackClient(host="http://google.com", port=80)

    assert client.url == "http://google.com:80"


@pytest.mark.parametrize(
    ("status_code", "output", "exception"),
    [(200, True, None), (404, False, None), (200, False, requests.ConnectionError)],
)
def test_client_healthcheck(
    starpack_client,
    requests_mock,
    status_code: int,
    output: bool,
    exception: Optional[Exception],
):
    url = "http://localhost:1976/healthcheck"
    if exception:
        requests_mock.get(url, exc=exception)
    else:
        requests_mock.get(url, text="nice", status_code=status_code)
    assert starpack_client.check_health() == output


@pytest.mark.parametrize(
    ("status_code", "output"),
    [(200, "http://localhost:2000"), (500, "500"), (300, "300")],
)
def test_client_deploy(
    starpack_client, requests_mock, capsys, status_code: int, output: str
):
    url = "http://localhost:1976/deploy"
    payload = {"deployment": {"metadata": {"name": "test"}}}
    requests_mock.post(
        url,
        status_code=status_code,
        json={"endpoints": {"fastapi": "http://localhost:2000"}},
    )
    starpack_client.deploy(payload)
    print_out = capsys.readouterr().out

    assert output in print_out


@pytest.mark.parametrize(
    ("status_code", "output"),
    [(200, "Successfully packaged"), (500, "500"), (300, "300")],
)
def test_client_package(
    starpack_client, requests_mock, capsys, status_code: int, output: str
):
    url = "http://localhost:1976/package"
    payload = {"package": {"metadata": {"name": "test"}}}
    requests_mock.post(url, status_code=status_code, text="")
    starpack_client.package(payload)
    print_out = capsys.readouterr().out

    assert output in print_out
