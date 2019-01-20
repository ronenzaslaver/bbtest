
"""
Test different command types (built in, python script etc...) on different hosts.

The destination host is set by
"""

import pytest
import subprocess

from tests.mytodo_box import MyToDoBox
from bbtest import BBPytest


class TestHosts(BBPytest):

    def test_builtin_command(self, topo):
        host = self.lab.hosts['host1']
        kwargs = {}
        if host.is_winodws_host():
            kwargs['shell'] = True
        assert host.run(['echo', 'Hello'], **kwargs) == ['Hello']

    def test_python_script(self, topo):
        # Test no output.
        box = self.lab.boxes[MyToDoBox.NAME][0]
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
