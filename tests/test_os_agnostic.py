
import pytest

import subprocess

from bbtest import BBTestCase
from .mytodo_box import MyToDoBox


class TestOsAgnostic(BBTestCase):

    LAB = {
        'host1': {
            'class': None,
            'boxes': [MyToDoBox],
         },
    }

    address_book = {'host1': {'ip': None, 'auth': None}}

    def test_operations(self, lab):
        # Test no output.
        box = lab.boxes[MyToDoBox.NAME][0]
        assert box.do_nothing() == []
        # Test output capture.
        box.add('Foo')
        todos = box.list()
        assert len(todos) == 1
        assert todos[0] == 'Foo'
        box.delete('Foo')
        todos = box.list()
        # Test error.
        assert len(todos) == 0
        with pytest.raises(subprocess.SubprocessError) as _:
            box.add('')
