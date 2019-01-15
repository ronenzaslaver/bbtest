
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
    parser.addoption('--os', action='store', default='local', help='OS type of traget machine - local, windows or linux')
    parser.addoption('--ip', action='store', default='', help='IP address of target machine')
    parser.addoption('--user', action='store', default='', help='Username for target machine')
    parser.addoption('--pw', action='store', default='', help='Password for target machine')


def pytest_configure(config):
    BaseToDoTest.LAB['host1']['class'] = os_2_class[config.getoption('--os')]
    BaseToDoTest.address_book['host1']['ip'] = config.getoption('--ip')
    BaseToDoTest.address_book['host1']['auth'] = (config.getoption('--user'), config.getoption('--pw'))
