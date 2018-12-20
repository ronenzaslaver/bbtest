
from bbtest import BBTestCase, LocalHost, BlackBox


class EmptyBox(BlackBox):
    NAME = 'empty'


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

    def test_hello_world(self):
        pass


class TestSingleBox(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [EmptyBox]
         },
    }

    def test_hello_world(self):
        pass


class MultiBox(BBTestCase):
    """ Do we allow/need Host without Box? """

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [EmptyBox, EmptyBox]
         },
    }

    def test_hello_world(self):
        pass
