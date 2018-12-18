import logging
from unittest import TestCase

from bbtest import Lab

logger = logging.getLogger('bblog')


class BBTestCase(TestCase):
    """A black box test case based on :class:`TestCase` """

    address_book = {}

    def setUp(self):
        """setups a lab for black box testing. """
        super().setUp()
        logger.setLevel(logging.DEBUG)
        if hasattr(self, 'LAB'):
            self.lab = Lab(self.LAB, address_book=self.address_book)

    def tearDown(self):
        self.lab.clean()
        super().tearDown()
