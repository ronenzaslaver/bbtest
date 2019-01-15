
import subprocess

from bbtest import BBTestCase
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
        self.assertEqual(box.do_nothing(), [])
        box.add('Foo')
        todos = box.list()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0], 'Foo')
        box.delete('Foo')
        todos = box.list()
        self.assertEqual(len(todos), 0)
        self.assertRaises(subprocess.SubprocessError, box.add, '')
