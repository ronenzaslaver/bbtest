""" How to test a todo?

This Module includes the test suite that verifies the todo component using
a black box methodology.

"""
from bbtest.testcase import BBTestCase

from crboxes.servers import TransparencyBox, RegistryBox


class CRTestCase(BBTestCase):
    pass


class LabTest(CRTestCase):

    LAB = {
        'ep': {
            'image': "linux",
            'boxes': [],
         },
        'server': {
            'image': "linux",
            'boxes': [TransparencyBox, RegistryBox],
         },
    }

    def test_install(self):
        ep_host = self.lab.hosts['ep']
        transparency_url = self.lab.boxes['transparency'].url
        registery_url = self.lab.boxes['registery'].url
        # Print the EP IP address.
        print(ep_host.ip)
        # Install sensor on EP.
        ep_host.install('/path/to/installer/dist/',
                        {'transparency': transparency_url,
                         'registry': registery_url})
        self.assertTrue(ep_host.path.isfile('file'))
        try:
            self.assertEqual(ep_host.registry('entry'), 'value')
        except NotImplemented:
            pass
