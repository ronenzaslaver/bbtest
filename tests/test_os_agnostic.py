
import sys
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


class ToDoTestLocalHost(BaseToDoTest):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [MyToDoBox],
         },
    }

    def test_operations(self):
        self._test_operations()


class ToDoTestWindowsHost(BaseToDoTest):

    LAB = {
        'host1': {
            'class': WindowsHost,
            'boxes': [MyToDoBox],
         },
    }

    address_book = {'host1': {'ip': 'localhost',
                              'auth': ('Administrator', 'Password1')}}

    @pytest.mark.skipif('win' not in sys.platform,
                        reason='Windows Test')
    def test_operations(self):
        self._test_operations()


class ToDoTestLinuxHost(BaseToDoTest):

    LAB = {
        'host1': {
            'class': LinuxHost,
            'boxes': [MyToDoBox],
         },
    }

    address_book = {'host1': {'ip': '127.0.0.1',
                              'auth': ('root', 'Password1')}}

    @pytest.mark.skipif(sys.platform != 'linux',
                        reason='Windows Test')
    def test_operations(self):
        self._test_operations()
