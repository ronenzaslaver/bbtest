
import os
import filecmp

from bbtest import BBTestCase, LocalHost, HomeBox, BaseHost
from cybereason.services.ecosystem import FileServer


class TestHomeBox(BBTestCase):
    """ Test basic methods - install, clean, remove.

    This test can run only on LocalHost.
    """

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [HomeBox, HomeBox],
         },
    }

    def tearDown(self):
        assert os.path.exists(TestHomeBox.empty_file_1)
        super().tearDown()
        assert not os.path.exists(TestHomeBox.empty_file_1)

    @classmethod
    def tearDownClass(cls):
        assert os.path.isdir(TestHomeBox.empty_box_1.path)
        super().tearDownClass()
        assert not os.path.isdir(TestHomeBox.empty_box_1.path)

    def test_home_box(self):
        empty_box_0 = self.lab.boxes[HomeBox.NAME][0]
        TestHomeBox.empty_box_1 = self.lab.boxes[HomeBox.NAME][1]
        assert os.path.isdir(empty_box_0.path)
        assert os.path.isdir(TestHomeBox.empty_box_1.path)
        assert empty_box_0.path != TestHomeBox.empty_box_1
        empty_file_0 = os.path.join(empty_box_0.path, 'empty')
        TestHomeBox.empty_file_1 = os.path.join(TestHomeBox.empty_box_1.path, 'empty')
        open(empty_file_0, 'a').close()
        open(TestHomeBox.empty_file_1, 'a').close()
        assert os.path.exists(empty_file_0)
        assert os.path.exists(TestHomeBox.empty_file_1)
        empty_box_0.clean()
        assert not os.path.exists(empty_file_0)
        empty_box_0.uninstall()
        assert not os.path.isdir(empty_box_0.path)


# FileServer is currently outside bbtest so ignore this tests.
class TestFileServer(BBTestCase):
    """ Test basic methods - put and get.

    This test can run only on LocalHost.
    """

    def setUp(self):
        host = BaseHost('127.0.0.1')
        self.file_server = FileServer(host=host, root_dir='/tmp/')

    def _test_basic_operations(self):
        source = os.path.join(os.path.dirname(__file__), 'src', 'mytodo.py')
        temp_mytodo = '/tmp/mytodo.py'
        destination = self.file_server.put(source, 'mytodo.py')
        assert os.path.exists(destination)
        self.file_server.get('mytodo.py', temp_mytodo)
        assert filecmp.cmp(source, temp_mytodo)
        os.remove(temp_mytodo)
        content = self.file_server.get('mytodo.py')
        with open(temp_mytodo, 'w') as f:
            f.write(content)
        assert filecmp.cmp(source, temp_mytodo)
