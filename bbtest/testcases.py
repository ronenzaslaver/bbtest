
"""
Base classes for black box tests - one for pytest and one for unittest derived tests.

The base classes should be identical so unittest users and pytest users will get the exact same services from the
infrastructure.
"""

import logging
import unittest

from bbtest import Lab


logger = logging.getLogger('bblog')


class BBPytest(object):
    """ Base class for black box tests for pytest tests.

    The setup/teardown methods within this class should be called from fixtures.
    A default conftest file with default fixtures can be found under the tests sample folder.

    We've added a class property `topo` that holds a dictionary defining the lab environment.
    Each test case can define a `topo` property used to setup a lab and store it in `self.lab`.
    """

    topo = {}
    address_book = {}
    lab = None

    @classmethod
    def create_lab(cls):
        """ Setups lab for black box testing. """
        logger.setLevel(logging.DEBUG)
        cls.lab = Lab(topology=cls.topo, address_book=cls.address_book)

    @classmethod
    def destroy_lab(cls):
        """ Destroy black box testing lab. """
        if cls.lab:
            cls.lab.destroy()

    def setup_lab(self):
        """ Setup black box testing lab before test cases. """
        pass

    def clean_lab(self):
        """ Clean black box testing lab after test cases. """
        if self.lab:
            self.lab.clean()


class BBTestCase(unittest.TestCase):
    """A black box test case based on :class:`unittest.TestCase`

    unitest calls the setup/teardown classes within this base class automatically.

    We've added a class property `topo` that holds a dictionary defining the lab enviornment.
    Each test case can define a `topo` property used to setup a lab and store it in `self.lab`.
    """

    topo = {}
    address_book = {}
    lab = None

    @classmethod
    def setUpClass(cls):
        """ Setups lab for black box testing. """
        logger.setLevel(logging.DEBUG)
        cls.lab = Lab(topology=cls.topo, address_book=cls.address_book)

    @classmethod
    def tearDownClass(cls):
        """ Destroy black box testing lab. """
        if cls.lab:
            cls.lab.destroy()

    def setUp(self):
        """ Setup black box testing lab between test cases. """
        if self.lab:
            self.lab.clean()

    def tearDown(self):
        """ Clean black box testing lab between test cases. """
        if self.lab:
            self.lab.clean()
