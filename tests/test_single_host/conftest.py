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
    ep_os = request.param.get('ep-os', 'local')
    ep_ip = request.param.get('ep-ip', 'localhost')
    pip_index = request.param.get('pip-index', None)
    request.cls.topo['hosts']['host1']['class'] = os_2_class[ep_os]
    request.cls.address_book['host1']['ip'] = ep_ip
    request.cls.topo['pip_index'] = pip_index


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--topo'):
        with open(metafunc.config.getoption('--topo')) as f:
            topos = yaml.safe_load(f)
    else:
        topos = [{'pip_index': metafunc.config.getoption('--pip-index'),
                  'os': metafunc.config.getoption('--ep-os'),
                  'ip': metafunc.config.getoption('--ep-ip')}]
    metafunc.parametrize('topo', topos, indirect=True)
