import pytest

#def pytest_addoption(parser):
#    parser.addoption("--product", action="store", default="default product")
#    parser.addoption("--input2", action="store", default="default input2")

@pytest.fixture(scope='session')
def command(target):
    shell = target.get_driver('CommandProtocol')
    target.activate(shell)
    return shell


def pytest_addoption(parser):
    parser.addoption(
        "--product", action="store", default="type1", help="my option: type1 or type2"
    )


@pytest.fixture
def product(request):
    return request.config.getoption("--product")
