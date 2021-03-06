
"""
Test operations on remote hosts.
- command types - built in, python script etc...
- get/set/copy files

The destination host (==topo) is set by pytest.
"""

import pytest
import subprocess
import os
import pathlib

from bbtest import RemoteHost, LocalHost, BBPytest, HomeBox, BaseHost
from tests.test_utils import get_temp_dir
from tests.mytodo_box import MyToDoBox


class TestHosts(BBPytest):

    topo = {
        'pip_index': 'will be set by pytest from topo yaml',
        'hosts': {
            'host1': {
                'class': 'will be set by pytest from topo yaml',
                'package': 'bbtest',
                'boxes': {
                    'box1': {'class': HomeBox}
                }
            }
        }
    }

    address_book = {'host1': {'ip': 'will be set by pytest from topo yaml'}}

    def setup(self):
        self.host = self.lab.hosts['host1']
        self.box = self.lab.hosts['host1'].boxes['box1']

    def test_builtin_command(self):
        kwargs = {}
        # todo move to hosts...
        if self.host.is_windows:
            kwargs['shell'] = True
        assert self.box.run(['echo', 'Hello'], **kwargs) == ['Hello']

    def test_python_commands(self):
        assert '3' in self.host.run_python3(['--version'])[0]
        # Fun fact - python --version prints the output to stderr so the output is empty string...
        assert self.host.run_python2(['--version']) == []

    def test_python_script(self):
        # Test no output.
        box = self.lab.add_box(MyToDoBox, self.host, 'my_todo')
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
        local_temp_file = self._create_temp_file()
        dest_temp_file = self.host.put(local_temp_file, 'temp_file')
        assert self.host.modules.os.path.isfile(dest_temp_file)
        os.remove(local_temp_file)
        self.host.get('temp_file', local_temp_file)
        assert os.path.isfile(local_temp_file)
        os.remove(local_temp_file)
        self.host.modules.os.remove(dest_temp_file)
        assert not self.host.modules.os.path.isfile(dest_temp_file)

    def test_box_put_get_files(self):
        local_temp_file = self._create_temp_file()
        self.box.put(local_temp_file, 'temp_file')
        assert self.box.isfile('temp_file')
        os.remove(local_temp_file)
        self.box.get('temp_file', local_temp_file)
        assert os.path.isfile(local_temp_file)
        os.remove(local_temp_file)
        self.box.rmfile('temp_file')
        assert not self.box.isfile('temp_file')

    @pytest.mark.xfail
    # Download is for URL downloads? need to better define the download_file and then better test.
    def test_download_files(self):
        local_temp_file = self._create_temp_file()
        dest_temp_file = os.path.join(self.host.root_path, 'temp_file')
        self.host.download_file(pathlib.Path(local_temp_file), dest_temp_file)
        assert self.host.modules.os.path.isfile(dest_temp_file)
        assert self.host.modules.os.path.getsize(dest_temp_file) == 1024
        os.remove(local_temp_file)
        self.host.modules.os.remove(dest_temp_file)

    def test_box_download_file(self):
        """ todo Create blackbox.download_file() and test similar to box get/put. """
        pass

    def test_timeout(self):
        # Test timeout on run command.
        self.host.run_python3(['-c', 'import time; time.sleep(2)'])
        with pytest.raises(Exception) as _:
            self.host.run_python3(['-c', 'import time; time.sleep(2)'], timeout=1)
        if self.host.is_remote:
            with pytest.raises(Exception) as _:
                self.host.run_python3(['-c', 'import time; time.sleep(2)'], sync_request_timeout=1)
        else:
            self.host.run_python3(['-c', 'import time; time.sleep(2)'], sync_request_timeout=1)

        # Test timeout on modules command.
        self.host.modules.time.sleep(2)
        self.host.set_client_timeout(1)
        if self.host.is_remote:
            with pytest.raises(Exception) as _:
                self.host.modules.time.sleep(2)
        else:
            self.host.modules.time.sleep(2)

    def test_host_properties(self):
        assert self.host.os in ['windows', 'linux']
        assert self.host.os_bits in [32, 64]
        assert self.host.platform in ['windows', 'debian', 'centos', 'ubuntu']
        assert self.host.is_local is not self.host.is_remote
        assert isinstance(self.host, LocalHost) != self.host.is_remote
        assert isinstance(self.host, RemoteHost) != self.host.is_local

    def _create_temp_file(self):
        local_temp_file = os.path.join(get_temp_dir(), 'temp_file')
        with open(local_temp_file, 'wb') as f:
            f.write(os.urandom(1024))
        return local_temp_file
