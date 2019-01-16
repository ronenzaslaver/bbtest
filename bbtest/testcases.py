import logging
import unittest

from bbtest import Lab

logger = logging.getLogger('bblog')


class BBTestCase(object):
    """A black box test case based on :class:`unittest.TestCase`

    We've added a class property `LAB` that holds a dictionary defining the lab enviornment.
    Each test case can define a `LAB` property used to setup a lab and store it in `self.lab`.
    """

    address_book = {}

    def setup(self):
        if hasattr(self, 'lab'):
            self.lab.clean()

    def teardown(self):
        if hasattr(self, 'lab'):
            self.lab.clean()

    @classmethod
    def setup_class(cls):
        """Setups a lab for black box testing. """
        logger.setLevel(logging.DEBUG)
        if hasattr(cls, 'LAB'):
            cls.lab = Lab(cls.LAB, address_book=cls.address_book)

    @classmethod
    def teardown_class(cls):
        if hasattr(cls, 'lab'):
            cls.lab.destroy()
