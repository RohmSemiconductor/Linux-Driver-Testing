import pytest

#def pytest_addoption(parser):
#    parser.addoption("--product", action="store", default="default product")
#    parser.addoption("--input2", action="store", default="default input2")

@pytest.fixture(scope='session')
def command(target):
    shell = target.get_driver('CommandProtocol')
    target.activate(shell)
    return shell

#def pytest_addoption(parser):
#    parser.addoption(
#        "--product", action="store", default="type1", help="my option: type1 or type2"
#    )

def pytest_addoption(parser):
    parser.addoption(
        "--power_port", action="store", default="type1", help="my option: type1 or type2"
    )
    parser.addoption(
        "--product", action="store", default="type1", help="my option: type1 or type2"
    )
    parser.addoption(
        "--beagle", action="store", default="type1", help="my option: type1 or type2"
    )

@pytest.fixture
def product(request):
    return request.config.getoption("--product")
@pytest.fixture
def power_port(request):
    return request.config.getoption("--power_port")
@pytest.fixture
def beagle(request):
    return request.config.getoption("--beagle")
