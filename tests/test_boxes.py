
import os
import pytest

from bbtest import BBPytest, LocalHost, HomeBox


class TestHomeBox(BBPytest):
    """ Test basic methods - install, clean, remove.

    This test can run only on LocalHost.

    :todo: add tests for default fixtures.
    """

    topo = {
        'hosts': {
            'host1': {
                'class': LocalHost,
                'boxes': [HomeBox, HomeBox]
            }
        }
    }

    def test_home_box(self):
        empty_box_0 = self.lab.boxes[HomeBox.NAME][0]
        empty_box_1 = self.lab.boxes[HomeBox.NAME][1]
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
