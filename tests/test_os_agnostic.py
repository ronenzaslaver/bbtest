
from bbtest import BBTestCase, LocalHost, LinuxHost, WindowsHost
from .mytodo_box import MyToDoBox


class BaseToDoTest(BBTestCase):

    def _test_operations(self):
        box = self.lab.boxes[MyToDoBox.NAME][0]
        box.add("Foo")
        todos = box.list()
        self.assertEqual(todos, ['Foo'])


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

    address_book = {'host1': {'ip': 'localhost'}}

    def test_operations(self):
        self._test_operations()


class ToDoTestLinuxHost(BaseToDoTest):

    LAB = {
        'host1': {
            'class': LinuxHost,
            'boxes': [MyToDoBox],
         },
    }

    def _test_operations(self):
        self._test_operations()
