
import pytest

from bbtest import BBTestCase, LocalHost, BlackBox, BaseHost
from bbtest.exceptions import ImproperlyConfigured


@pytest.fixture(scope='class')
def lab(request):
    request.cls.setup_lab()
    yield request.cls.lab
    request.cls.teardown_lab()


class EmptyBox(BlackBox):
    NAME = 'empty'


class YetAnotherEmptyBox(BlackBox):
    NAME = 'yetanotherempty'


class TestNoLab(BBTestCase):

    def test_no_lab(self, lab):
        pass


class TestNoClass(BBTestCase):

    LAB = {
        'host1': {
            'boxes': []
         },
    }

    @classmethod
    def setup_lab(cls):
        with pytest.raises(ImproperlyConfigured) as _:
            super().setup_lab()

    def test_no_class(self, lab):
        pass


class TestBaseHost(BBTestCase):

    LAB = {
        'host1': {
            'class': BaseHost,
            'boxes': []
         },
    }

    def test_base_host(self, lab):
        pass


class TestNoBox(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': []
         },
    }

    def test_no_box(self, lab):
        pass


class TestSingleBox(BBTestCase):

    LAB = {
        'host1': {
            'class': LocalHost,
            'boxes': [EmptyBox]
         },
    }

    def test_single_box(self, lab):
        assert len(lab.boxes[EmptyBox.NAME]) == 1
        assert lab.boxes[EmptyBox.NAME][0].host.ip == '127.0.0.1'


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

    def test_multi_boxes(self, lab):
        assert len(lab.boxes[EmptyBox.NAME]) == 2
        assert len(lab.boxes[YetAnotherEmptyBox.NAME]) == 2
