
import pytest

from bbtest import BBPytest, LocalHost, BlackBox, BaseHost, Lab
from bbtest.exceptions import ImproperlyConfigured


class EmptyBox(BlackBox):
    NAME = 'empty'


class YetAnotherEmptyBox(BlackBox):
    NAME = 'yetanotherempty'


class TestNoLab(BBPytest):

    def test_no_lab(self):
        pass


class TestImproperlyConfigured(BBPytest):

    topo = {
        'host1': {
         },
    }

    @pytest.fixture(scope='class', autouse=True)
    def lab_factory(request):
        with pytest.raises(ImproperlyConfigured) as _:
            Lab(request.topo)
        request.topo['host1']['class'] = BaseHost
        with pytest.raises(ImproperlyConfigured) as _:
            Lab(request.topo)
        request.topo['host1']['boxes'] = []
        Lab(request.topo)

    def test_no_class(self):
        pass


class TestBaseHost(BBPytest):

    topo = {
        'host1': {
            'class': BaseHost,
            'boxes': []
         },
    }

    def test_base_host(self):
        pass


class TestNoBox(BBPytest):

    topo = {
        'host1': {
            'class': LocalHost,
            'boxes': []
         },
    }

    def test_no_box(self):
        pass


class TestSingleBox(BBPytest):

    topo = {
        'host1': {
            'class': LocalHost,
            'boxes': [EmptyBox]
         },
    }

    def test_single_box(self):
        assert len(self.lab.boxes[EmptyBox.NAME]) == 1
        assert self.lab.boxes[EmptyBox.NAME][0].host.ip == '127.0.0.1'


class MultiBox(BBPytest):

    topo = {
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
