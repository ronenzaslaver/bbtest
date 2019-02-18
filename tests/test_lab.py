"""
Basic lab tests - create lab from topology, cleanup and destroy lab, default fixtures or classical unittest...

This tests can run only on LocalHost.
"""

import os
import pytest
import socket

from bbtest import BBTestCase, HomeBox, BBPytest, LocalHost, BlackBox, BaseHost, Lab
from bbtest.exceptions import ImproperlyConfigured


class EmptyBox(BlackBox):
    pass


class YetAnotherEmptyBox(BlackBox):
    pass


class TestNoLab(BBPytest):

    def test_no_lab(self):
        pass


class TestImproperlyConfigured(BBPytest):

    topo = {
        'hosts': {
            'host1': {
            }
        }
    }

    @pytest.fixture(scope='class', autouse=True)
    def lab_factory(request):
        with pytest.raises(ImproperlyConfigured) as _:
            Lab(request.topo)
        request.topo['hosts']['host1']['class'] = BaseHost
        Lab(request.topo)

    def test_no_class(self):
        pass


class TestBaseHost(BBPytest):

    topo = {
        'hosts': {
            'host1': {
                'class': LocalHost,
                'yet_another_param': 'yet_another_value'
            }
        }
    }

    def test_host_name_and_params(self):
        host = self.lab.hosts['host1']
        assert host.name == 'host1'
        assert str(host) == 'host1'
        assert host.ip == '127.0.0.1'
        assert host.params['yet_another_param'] == 'yet_another_value'
        assert self.lab.hosts['host1'].hostname == socket.gethostname()


class TestNoBox(BBPytest):

    topo = {
        'hosts': {
            'host1': {
                'class': LocalHost,
                'boxes': {}
            }
        }
    }

    def test_empty_box(self):
        pass


class TestMultiHosts(BBPytest):

    topo = {
        'hosts': {
            'host1': {
                'class': LocalHost,
                'boxes': {
                    'homebox': {'class': HomeBox},
                    'emptybox': {'class': EmptyBox}
                }
            },
            'host2': {
                'class': LocalHost,
                'boxes': {
                    'homebox': {'class': HomeBox},
                    'emptybox': {'class': EmptyBox}
                }
            }
        }
    }

    def test_multi_boxes(self):
        assert len(self.lab.hosts) == 2
        assert len(self.lab.boxes) == 4
        assert self.lab.hosts['host1'].boxes['homebox'] == self.lab.boxes['host1.homebox']
        assert len(self.lab.class_boxes(HomeBox)) == 2


class TestBBTestCase(BBTestCase):
    """ Test classical unittest.TestCase - empty (no) fixtures, rely on setup/teardown. """

    # Nullifies the pytest conftest and let unittest.TestCase kick in.
    @pytest.fixture(scope='class', autouse=True)
    def lab_factory(request):
        pass

    @pytest.fixture(autouse=True)
    def clean_lab_factory(request):
        pass

    topo = {
        'hosts': {
            'host1': {
                'class': LocalHost,
                'yet_another_param': 'yet_another_value'
            }
        }
    }

    def test_host_name_and_params(self):
        host = self.lab.hosts['host1']
        assert host.name == 'host1'
        assert str(host) == 'host1'
        assert host.ip == '127.0.0.1'
        assert host.params['yet_another_param'] == 'yet_another_value'
        assert self.lab.hosts['host1'].hostname == socket.gethostname()


class TestHomeBox(BBPytest):

    topo = {
        'hosts': {
            'host1': {
                'class': LocalHost,
                'boxes': {
                    'homebox0': {'class': HomeBox,
                                 'yet_another_param': 'yet_another_value_0'},
                    'homebox1': {'class': HomeBox,
                                 'yet_another_param': 'yet_another_value_1'}
                }
            }
        }
    }

    def test_box_name_and_params(self):
        empty_box_0 = self.lab.boxes['host1.homebox0']
        assert empty_box_0.name == 'homebox0'
        assert str(empty_box_0) == 'homebox0'
        assert type(empty_box_0.host) == LocalHost
        assert empty_box_0.params['yet_another_param'] == 'yet_another_value_0'

    def test_two_boxes(self):
        empty_box_0 = self.lab.boxes['host1.homebox0']
        empty_box_1 = self.lab.boxes['host1.homebox1']
        assert empty_box_0.params['yet_another_param'] != empty_box_1.params['yet_another_param']
        assert os.path.isdir(empty_box_0.path)
        assert os.path.isdir(empty_box_1.path)
        assert empty_box_0.path != empty_box_1
        empty_file_0 = os.path.join(empty_box_0.path, 'empty')
        empty_file_1 = os.path.join(empty_box_1.path, 'empty')
        sub_dir_0 = os.path.join(empty_box_0.path, 'subdir')
        sub_dir_1 = os.path.join(empty_box_1.path, 'subdir')
        open(empty_file_0, 'a').close()
        open(empty_file_1, 'a').close()
        os.mkdir(sub_dir_0)
        os.mkdir(sub_dir_1)
        assert os.path.exists(empty_file_0)
        assert os.path.exists(empty_file_1)
        assert os.path.isdir(sub_dir_0)
        assert os.path.isdir(sub_dir_1)
        empty_box_0.clean()
        assert not os.path.exists(empty_file_0)
        assert os.path.exists(empty_file_1)
        assert not os.path.isdir(sub_dir_0)
        assert os.path.isdir(sub_dir_1)
        empty_box_0.uninstall()
        assert not os.path.isdir(empty_box_0.path)
