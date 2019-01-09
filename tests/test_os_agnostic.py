
import pytest

from bbtest import BBTestCase, LocalHost, LinuxHost, WindowsHost
from .mytodo_box import MyToDoBox


class BaseToDoTest(BBTestCase):

    LAB = {
        'host1': {
            'class': None,
            'boxes': [MyToDoBox],
         },
    }

    address_book = {'host1': {'ip': None, 'auth': None}}

    def test_operations(self):
        box = self.lab.boxes[MyToDoBox.NAME][0]
        box.add('Foo')
        todos = box.list()
        self.assertEquals(len(todos), 1)
        self.assertEquals(todos[0], 'Foo')
