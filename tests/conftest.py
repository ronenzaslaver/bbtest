
import pytest

from bbtest import LocalHost, WindowsHost, LinuxHost, OSXHost
from tests.test_os_agnostic import BaseToDoTest

os_2_class = {'local': LocalHost,
              'win': WindowsHost,
              'windows': WindowsHost,
              'win32': WindowsHost,
              'linux': LinuxHost,
              'mac': OSXHost,
              'osx': OSXHost}


def pytest_addoption(parser):
    parser.addoption('--os', action='store', default='local',
                     help='OS of target machine - local, windows, linux, mac or config')
    parser.addoption('--ip', action='store', default='172.16.30.164', help='IP address of target machine')
    parser.addoption('--user', action='store', default='root', help='Username for target machine')
    parser.addoption('--pw', action='store', default='Password1', help='Password for target machine')


def pytest_configure(config):
    BaseToDoTest.LAB['host1']['class'] = os_2_class[config.getoption('--os')]
    BaseToDoTest.address_book['host1']['ip'] = config.getoption('--ip')
    BaseToDoTest.address_book['host1']['auth'] = (config.getoption('--user'), config.getoption('--pw'))

"""

todo - test if works when not extending unittest.TestCase

@pytest.fixture
def os(request):
    print('in os fixture')
    pass


def pytest_generate_tests(metafunc):
    print('in pytest_generate_tests')
    oss = [metafunc.config.getoption('--os')]
    metafunc.parametrize('os', 'local', indirect=True)

"""
