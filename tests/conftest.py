
import pytest

from bbtest import LocalHost, WindowsHost, LinuxHost, OSXHost


os_2_class = {'local': LocalHost,
              'win': WindowsHost,
              'windows': WindowsHost,
              'win32': WindowsHost,
              'linux': LinuxHost,
              'mac': OSXHost,
              'osx': OSXHost}


def pytest_addoption(parser):
    parser.addoption('--os', action='store', default='local', help='OS of target machine - local, windows, linux oe mac')
    parser.addoption('--config', action='store', default='config', help='path to configuration file')
    parser.addoption('--ip', action='store', default='', help='IP address of target machine')
    parser.addoption('--user', action='store', default='', help='Username for target machine')
    parser.addoption('--pw', action='store', default='', help='Password for target machine')


@pytest.fixture(scope='class')
def lab(request):
    request.cls.LAB['host1']['class'] = os_2_class[request.param[0]]
    request.cls.address_book['host1']['ip'] = request.param[1]
    request.cls.address_book['host1']['auth'] = (request.param[2][0], request.param[2][1])
    request.cls.setup_lab()
    yield request.cls.lab
    request.cls.teardown_lab()


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--config'):
        hosts = [['local', '', ('', '')], ['win', 'localhost', ('', '')]]
    else:
        hosts = [metafunc.config.getoption('--os'), metafunc.config.getoption('--ip'),
                (metafunc.config.getoption('--user'), metafunc.config.getoption('--pw'))]
    metafunc.parametrize('lab', hosts, indirect=True)
