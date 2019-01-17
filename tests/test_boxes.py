
import os
import pytest

from bbtest import BBTestCase, LocalHost, HomeBox, BaseHost


@pytest.fixture(scope='class')
def lab(request):
    request.cls.setup_lab()
    yield request.cls.lab
    request.cls.teardown_lab()


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

    def teardown(self):
        assert os.path.exists(TestHomeBox.empty_file_1)
        super().teardown()
        assert not os.path.exists(TestHomeBox.empty_file_1)

    @classmethod
    def teardown_lab(cls):
        assert os.path.isdir(TestHomeBox.empty_box_1.path)
        super().teardown_lab()
        assert not os.path.isdir(TestHomeBox.empty_box_1.path)

    def test_home_box(self, lab):
        empty_box_0 = lab.boxes[HomeBox.NAME][0]
        TestHomeBox.empty_box_1 = lab.boxes[HomeBox.NAME][1]
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
