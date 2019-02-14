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


@pytest.fixture(scope='class')
def topo(request):
    request.cls.topo['pip_index'] = request.param.get('pip-index', None)
    request.cls.topo['hosts']['host1']['class'] = os_2_class[request.param['ep-os']]
    request.cls.address_book['host1']['ip'] = request.param['ep-ip']


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--topo'):
        with open(metafunc.config.getoption('--topo')) as f:
            topos = yaml.safe_load(f)
    else:
        topos = [{'pip_index': metafunc.config.getoption('--pip-index'),
                  'os': metafunc.config.getoption('--ep-os'),
                  'ip': metafunc.config.getoption('--ep-ip')}]
    metafunc.parametrize('topo', topos, indirect=True)
