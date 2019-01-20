"""
conftest that accepts a single host as parameter (see bellow for details) to be used for all tests that require single host as input.
Note that the default create_destroy will be called anyway but as it works on empty topo it will have no effect.
"""

import pytest

from bbtest import LocalHost, WindowsHost, LinuxHost, OSXHost
from tests.mytodo_box import MyToDoBox


@pytest.fixture(scope='class', autouse=True)
def create_destroy(request, topo):
    request.cls.create_lab()
    yield


os_2_class = {'local': LocalHost,
              'win': WindowsHost,
              'windows': WindowsHost,
              'win32': WindowsHost,
              'linux': LinuxHost,
              'mac': OSXHost,
              'osx': OSXHost}


def pytest_addoption(parser):
    parser.addoption('--bbtopo', action='store', default='config', help='path to bbtest lab topology file')
    parser.addoption('--os', action='store', default='local', help='OS of target machine - local, windows, linux oe mac')
    parser.addoption('--ip', action='store', default='', help='IP address of target machine')
    parser.addoption('--user', action='store', default='', help='Username for target machine')
    parser.addoption('--pw', action='store', default='', help='Password for target machine')


@pytest.fixture(scope='class')
def topo(request):
    request.cls.topo = {'host1': {'class': os_2_class[request.param[0]],
                        'boxes': [MyToDoBox]}}
    request.cls.address_book = {'host1': {'ip': request.param[1],
                                'auth': (request.param[2][0], request.param[2][1])}}


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--bbtopo'):
        topos = [['local', '', ('', '')], ['win', 'localhost', ('', '')]]
    else:
        topos = [metafunc.config.getoption('--os'), metafunc.config.getoption('--ip'),
                (metafunc.config.getoption('--user'), metafunc.config.getoption('--pw'))]
    metafunc.parametrize('topo', topos, indirect=True)
