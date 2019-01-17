import unittest
from bbtest.hosts import LocalHost


class TestLocalHost(unittest.TestCase):
    def test_successful_run(self):
        host = LocalHost()
        kwargs = {}
        if host.is_winodws_host():
            kwargs['shell'] = True

        self.assertEqual(host.run(['echo', 'Hello'], **kwargs), ['Hello'])
