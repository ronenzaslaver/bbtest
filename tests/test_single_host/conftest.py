"""
conftest that accepts a single host as parameter (see bellow for details) to be used for all tests that require single host as input.
"""

import pytest
import yaml

from bbtest import LocalHost, WindowsHost, LinuxHost, OSXHost


@pytest.fixture(scope='class', autouse=True)
def lab_factory(request, topo):
    request.cls.create_lab()
    yield
    request.cls.destroy_lab()


os_2_class = {'local': LocalHost,
              'win': WindowsHost,
              'windows': WindowsHost,
              'win32': WindowsHost,
              'linux': LinuxHost,
              'mac': OSXHost,
              'osx': OSXHost}


def pytest_addoption(parser):
    parser.addoption('--topo', action='store', default='', help='path to bbtest lab topology file')
    parser.addoption('--os', action='store', default='win', help='OS of target machine - local, windows, linux oe mac')
    parser.addoption('--ip', action='store', default='localhost', help='IP address of target machine')
    parser.addoption('--user', action='store', default='', help='Username for target machine')
    parser.addoption('--pw', action='store', default='', help='Password for target machine')


@pytest.fixture(scope='class')
def topo(request):
    request.cls.topo = {'host1': {'class': os_2_class[request.param[0]],
                        'boxes': []}}
    request.cls.address_book = {'host1': {'ip': request.param[1],
                                'auth': (request.param[2], request.param[3])}}


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--topo'):
        with open(metafunc.config.getoption('--topo')) as f:
            topos_in = yaml.safe_load(f)
        topos = [list(t.values()) for t in topos_in]
    else:
        topos = [[metafunc.config.getoption('--os'), metafunc.config.getoption('--ip'),
                  metafunc.config.getoption('--user'), metafunc.config.getoption('--pw')]]
    metafunc.parametrize('topo', topos, indirect=True)
