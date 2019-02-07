"""
conftest that accepts a single host as parameter (see bellow for details) to be used for all tests that require single host as input.
"""

import pytest
import yaml
import os

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
    parser.addoption('--topo', action='store', default=os.environ.get('BBTEST_TOPO_YAML', ''), help='path to bbtest lab topology file')
    parser.addoption('--os', action='store', default='local', help='OS of target machine - local, windows, linux oe mac')
    parser.addoption('--ip', action='store', default='', help='IP address of target machine')
    parser.addoption('--user', action='store', default='', help='Username for target machine')
    parser.addoption('--pw', action='store', default='', help='Password for target machine')


@pytest.fixture(scope='class')
def topo(request):
    request.cls.topo = {'pip_index': request.param.get('pip-index', None),
                        'hosts': {'host1': {'class': os_2_class[request.param['os']],
                                            'package': 'bbtest',
                                            'boxes': []}}}
    request.cls.address_book = {'host1': {'ip': request.param['ip'],
                                          'auth': request.param.get('auth', None)}}


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--topo'):
        with open(metafunc.config.getoption('--topo')) as f:
            topos = yaml.safe_load(f)
    else:
        topos = [{'pip_index': metafunc.config.getoption('--pip-index'),
                  'os': metafunc.config.getoption('--os'),
                  'ip': metafunc.config.getoption('--ip'),
                  'auth': (metafunc.config.getoption('--user'), metafunc.config.getoption('--pw'))}]
    metafunc.parametrize('topo', topos, indirect=True)
