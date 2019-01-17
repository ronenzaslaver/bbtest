
import logging
import pytest


logger = logging.getLogger('bblog')


class BBTestCase(object):
    """A black box test case based on :class:`unittest.TestCase`

    We've added a class property `topo` that holds a dictionary defining the lab enviornment.
    Each test case can define a `topo` property used to setup a lab and store it in `self.lab`.
    """

    @pytest.fixture(autouse=True)
    def clean_lab(request):
        yield
        if hasattr(request, 'lab'):
            request.lab.clean()
