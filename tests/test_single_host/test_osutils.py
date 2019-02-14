
"""
Test bbtest OS utilities (bbtest.osutils) on different hosts.

The destination host (==topo) is set by pytest.
"""

import pytest
import subprocess
import os
import pathlib

from bbtest import RemoteHost, BBPytest, HomeBox


class TestHosts(BBPytest):

    topo = {
        'hosts': {
            'host1': {
                'class': 'will be set by pytest from topo yaml',
                'package': 'bbtest',
            }
        }
    }

    address_book = {'host1': {'ip': 'will be set by pytest from topo yaml'}}

    def setup(self):
        self.host = self.lab.hosts['host1']

    def test_is_process_running(self):
        assert not self.host.modules.bbtest.osutils.is_process_running('no-such-process')
        if self.host.is_linux:
            assert self.host.modules.bbtest.osutils.is_process_running('crond')
        else:
            assert self.host.modules.bbtest.osutils.is_process_running('svchost.exe')

    def test_is_service_running(self):
        assert not self.host.modules.bbtest.osutils.is_service_running('no-such-service')
        if self.host.is_linux:
            assert self.host.modules.bbtest.osutils.is_service_running('crond')
        else:
            assert self.host.modules.bbtest.osutils.is_service_running('Appinfo')
