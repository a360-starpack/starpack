import pytest

from starpack import __main__ as starpack_funcs

@pytest.mark.parametrize("resource", ("deployment", "model", "package"))
def test_list(resource: str):
    starpack_funcs.list_resources(resource)