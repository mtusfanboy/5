import pytest

pytest_plugins = ('anyio',)


@pytest.fixture(params=["asyncio"])
def anyio_backend():
    return "asyncio"
