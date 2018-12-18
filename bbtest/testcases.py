import logging
from unittest import TestCase

from bbtest import Lab

logger = logging.getLogger('bblog')


class BBTestCase(TestCase):
    """A black box test case based on :class:`TestCase` """

    address_book = {}

    @classmethod
    def setUpClass(cls):
        """setups a lab for black box testing. """
        super().setUpClass()
        logger.setLevel(logging.DEBUG)
        if hasattr(cls, 'LAB'):
            cls.lab = Lab(cls.LAB, address_book=cls.address_book)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'lab'):
            cls.lab.remove()

        super().tearDownClass()
