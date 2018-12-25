
import os

from bbtest import BBTestCase, LocalHost, HomeBox


class EmptyHomeBox(HomeBox):
    pass


class TestEmptyHomeBox(BBTestCase):
    """ Test basic methods - install, clean, remove """

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [EmptyHomeBox],
         },
    }

    def test_home_box(self):
        empty_box = self.lab.boxes[EmptyHomeBox.NAME][0]
        assert os.path.isdir(empty_box.path)
        empty_file = os.path.join(empty_box.path, 'empty')
        open(empty_file, 'a').close()
        assert os.path.exists(empty_file)
        empty_box.clean()
        assert not os.path.exists(empty_file)
