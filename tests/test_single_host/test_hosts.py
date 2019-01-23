
"""
Test different command types (built in, python script etc...) on different hosts.

The destination host is set by
"""

import pytest
import subprocess
import os

from tests.mytodo_box import MyToDoBox
from bbtest import BBPytest


class TestHosts(BBPytest):

    def setup(self):
        self.host = self.lab.hosts['host1']

    def test_builtin_command(self):
        kwargs = {}
        # todo move to hosts...
        if self.host.is_winodws():
            kwargs['shell'] = True
        assert self.host.run(['echo', 'Hello'], **kwargs) == ['Hello']

    def test_python_script(self):
        # Test no output.
        box = self.lab.add_box(MyToDoBox, self.host)
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

    def _test_put_get_files(self):
        """ Work in progress """
        host = self.lab.hosts['host1']
        temp_file = os.path.join(os.path.dirname(__file__), 'temp_file')
        with open(temp_file, 'wb') as f:
            f.write(os.urandom(1024))
        host.put(temp_file, temp_file)
        print(host.root_path)
        os.remove(temp_file)
