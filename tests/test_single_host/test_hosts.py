
"""
Test operations on remote hosts.
- command types - built in, python script etc...
- get/set/copy files

The destination host (==topo) is set by pytest.
"""

import pytest
import subprocess
import os

from bbtest import BBPytest
from tests.test_utils import get_temp_dir
from tests.mytodo_box import MyToDoBox

from artifactory import ArtifactoryPath


class TestHosts(BBPytest):

    def setup(self):
        self.host = self.lab.hosts['host1']

    def test_builtin_command(self):
        kwargs = {}
        # todo move to hosts...
        if self.host.is_winodws:
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

    def test_put_get_files(self):
        """ Work in progress """
        host = self.lab.hosts['host1']
        local_temp_file = os.path.join(get_temp_dir(), 'temp_file')
        with open(local_temp_file, 'wb') as f:
            f.write(os.urandom(1024))
        dest_temp_file = host.put(local_temp_file, 'temp_file')
        os.remove(local_temp_file)
        assert host.isfile(dest_temp_file)
        host.get('temp_file', local_temp_file)
        assert os.path.isfile(local_temp_file)
        os.remove(local_temp_file)
