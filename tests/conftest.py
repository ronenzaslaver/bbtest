
import pytest

from bbtest import LocalHost, WindowsHost, LinuxHost, OSXHost
from tests.test_os_agnostic import TestOsAgnostic

os_2_class = {'local': LocalHost,
              'win': WindowsHost,
              'windows': WindowsHost,
              'win32': WindowsHost,
              'linux': LinuxHost,
              'mac': OSXHost,
              'osx': OSXHost}


def pytest_addoption(parser):
    parser.addoption('--os', action='store', default='',
                     help='OS of target machine - local, windows, linux, mac or config')
    parser.addoption('--ip', action='store', default='172.16.30.164', help='IP address of target machine')
    parser.addoption('--user', action='store', default='root', help='Username for target machine')
    parser.addoption('--pw', action='store', default='Password1', help='Password for target machine')


def pytest_configure(config):
    print('in pytest_configure')
    TestOsAgnostic.address_book['host1']['ip'] = config.getoption('--ip')
    TestOsAgnostic.address_book['host1']['auth'] = (config.getoption('--user'), config.getoption('--pw'))


@pytest.fixture(scope='class')
def os(request):
    print('in fixture')
    request.cls.LAB['host1']['class'] = os_2_class[request.param]


def pytest_generate_tests(metafunc):
    print('in pytest_generate_tests')
    oss = [metafunc.config.getoption('--os')] if metafunc.config.getoption('--os') else ['local', 'win']
    metafunc.parametrize('os', oss, indirect=True)
