import unittest
from bbtest.hosts import LocalHost

class test_local_host(unittest.TestCase):
    def test_succesful_run(self):
        host = LocalHost()
        self.assertEqual(host.run('echo Hello World'), ['Hello World'])