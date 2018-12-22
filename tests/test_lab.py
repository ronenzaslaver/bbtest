
from bbtest import BBTestCase, LocalHost, BlackBox


class EmptyBox(BlackBox):
    NAME = 'empty'


class YetAnotherEmptyBox(BlackBox):
    NAME = 'yetanotherempty'


class TestNoLab(BBTestCase):

    def test_hello_world(self):
        pass


class TestNoBox(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': []
         },
    }

    def test_no_box(self):
        pass


class TestSingleBox(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [EmptyBox]
         },
    }

    def test_single_box(self):
        assert len(self.lab.boxes[EmptyBox.NAME]) == 1
        assert self.lab.boxes[EmptyBox.NAME][0].host.ip == 'localhost'


class MultiBox(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [EmptyBox, EmptyBox]
         },
        'host2': {
            'class': LocalHost,
            'boxes': [YetAnotherEmptyBox, YetAnotherEmptyBox]
         },
    }

    def test_multi_boxes(self):
        assert len(self.lab.boxes[EmptyBox.NAME]) == 2
        assert len(self.lab.boxes[YetAnotherEmptyBox.NAME]) == 2
