from starpack.client import StarpackClient
import pytest

@pytest.fixture
def starpack_client():
    client = StarpackClient()

    return client


# def test_client_package(client: StarpackClient):
#     client.package()
