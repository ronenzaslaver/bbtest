import unittest
from bbtest.hosts import LocalHost


class TestLocalHost(unittest.TestCase):
    def test_successful_run(self):
        host = LocalHost()
        self.assertEqual(host.run('echo', 'Hello World'), ['"Hello World"'])
