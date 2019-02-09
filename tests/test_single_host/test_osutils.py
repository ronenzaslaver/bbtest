
"""
Test bbtest OS utilities (bbtest.osutils) on different hosts.

The destination host (==topo) is set by pytest.
"""

import pytest
import subprocess
import os
import pathlib

from bbtest import RemoteHost, BBPytest, HomeBox
from tests.test_utils import get_temp_dir
from tests.mytodo_box import MyToDoBox


class TestHosts(BBPytest):

    def setup(self):
        self.host = self.lab.hosts['host1']

    def test_is_process_running(self):
        assert not self.host.modules.osutils.is_process_running('no-such-process')
        if self.host.is_remote:
            assert self.host.modules.osutils.is_process_running('rpyc_classic.py')
