
import pytest

from bbtest import LocalHost, WindowsHost, LinuxHost, OSXHost, Lab
from tests.mytodo_box import MyToDoBox


os_2_class = {'local': LocalHost,
              'win': WindowsHost,
              'windows': WindowsHost,
              'win32': WindowsHost,
              'linux': LinuxHost,
              'mac': OSXHost,
              'osx': OSXHost}


def pytest_addoption(parser):
    parser.addoption('--os', action='store', default='local', help='OS of target machine - local, windows, linux oe mac')
    parser.addoption('--bbtopo', action='store', default='config', help='path to bbtest lab topology file')
    parser.addoption('--ip', action='store', default='', help='IP address of target machine')
    parser.addoption('--user', action='store', default='', help='Username for target machine')
    parser.addoption('--pw', action='store', default='', help='Password for target machine')


@pytest.fixture(scope='class', autouse=True)
def manage_lab(request):
    topo = {'host1': {'class': os_2_class[request.param[0]],
                     'boxes': [MyToDoBox]}}
    address_book = {'host1': {'ip': request.param[1],
                              'auth': (request.param[2][0], request.param[2][1])}}
    request.cls.lab = Lab(topo, address_book)
    yield
    request.cls.lab.destroy()


def pytest_generate_tests(metafunc):
    if metafunc.config.getoption('--bbtopo'):
        topos = [['local', '', ('', '')], ['win', 'localhost', ('', '')]]
    else:
        topos = [metafunc.config.getoption('--os'), metafunc.config.getoption('--ip'),
                (metafunc.config.getoption('--user'), metafunc.config.getoption('--pw'))]
    metafunc.parametrize('manage_lab', topos, indirect=True)
