"""
"""

from bbtest import WindowsHost
from bbtest import BBTestCase

from cybereason.boxes.servers import TransparencyBox, RegistryBox, PerspectiveBox, PersonalizeBox
from bbtest.hosts import LinuxHost


class CRTestCase(BBTestCase):
    pass


class InstallTest(CRTestCase):

    """
    Maybe LAB should define boxes and for each box we set the Host? It would be great if we could ask the
    LAB service to allocate a Box instead of Host as many cases we don't care about the Host but the Box.
    Maybe we should have both ways?
    If we stay with the current structure - should we give up on the address book and define a given host in the LAB
        itself?
    Is there any way to avoid specifying the Host class (for a known Host) and let the LAB find it?
    """

    LAB = {
        'ep': {
            'class': WindowsHost,
            'boxes': [],
         },
        'repository': {
            'class': LinuxHost,
            'boxes': [],
         },
        'perspective': {
            'image': LinuxHost,
            'boxes': [PerspectiveBox],
         },
        'transparency': {
            'class': LinuxHost,
            'boxes': [TransparencyBox, RegistryBox, PersonalizeBox],
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
