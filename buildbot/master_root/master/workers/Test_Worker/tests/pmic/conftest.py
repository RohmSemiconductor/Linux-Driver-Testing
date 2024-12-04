import pytest

@pytest.fixture(scope='session')
def command(target):
    shell = target.get_driver('CommandProtocol')
    target.activate(shell)
    return shell

def pytest_addoption(parser):
    parser.addoption("--power_port", action="store", default="type1", help="my option: type1 or type2")
    parser.addoption("--product", action="store", default="type1", help="my option: type1 or type2")
    parser.addoption("--type", action="store", default="type1", help="my option: type1 or type2")
    parser.addoption("--beagle", action="store", default="type1", help="my option: type1 or type2")
    parser.addoption("--dts", action="store", default="default", help="my option: type1 or type2")
    parser.addoption("--kunit_test", action="store", default="linear_ranges", help="my option: linear_ranges or iio_gts_test")
    parser.addoption("--result_dir", action="store", default="linux", help="my option: linux, PMIC, or sensor")

@pytest.fixture
def type(request):
    return request.config.getoption("--type")
@pytest.fixture
def product(request):
    return request.config.getoption("--product")
@pytest.fixture
def power_port(request):
    return request.config.getoption("--power_port")
@pytest.fixture
def beagle(request):
    return request.config.getoption("--beagle")
@pytest.fixture
def dts(request):
    return request.config.getoption("--dts")
@pytest.fixture
def kunit_test(request):
    return request.config.getoption("--kunit_test")
@pytest.fixture
def result_dir(request):
    return request.config.getoption("--result_dir")
