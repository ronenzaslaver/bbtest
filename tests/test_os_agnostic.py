
import pytest

from bbtest import BBTestCase, LocalHost, LinuxHost, WindowsHost
from .mytodo_box import MyToDoBox


class BaseToDoTest(BBTestCase):

    def _test_operations(self):
        box = self.lab.boxes[MyToDoBox.NAME][0]
        box.add("Foo")
        todos = box.list()
        self.assertEquals(len(todos), 1)
        self.assertEquals(todos[0], "Foo")


class BaseToDoTest(BaseToDoTest):

    LAB = {
        'host1': {
            'class': None,
            'boxes': [MyToDoBox],
         },
    }

    address_book = {'host1': {'ip': None, 'auth': None}}

    os_2_class = {'local': LocalHost,
                  'win': WindowsHost,
                  'linux': LinuxHost}

    @classmethod
    def setUpClass(cls):
        cls.LAB['host1']['class'] = BaseToDoTest.os_2_class[pytest.config.getoption('--os')]
        cls.address_book['host1']['ip'] = pytest.config.getoption('--ip')
        cls.address_book['host1']['auth'] = (pytest.config.getoption('--user'), pytest.config.getoption('--pw'))
        super().setUpClass()

    def test_operations(self):
        self._test_operations()
