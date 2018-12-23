"""
"""

from bbtest import WindowsHost, LinuxHost
from bbtest import BBTestCase

from cybereason.boxes.servers import TransparencyBox, RegistryBox, PerspectiveBox, PersonalizationBox, DownloadBox
from cybereason.boxes.sensor import SensorBox
from cybereason.services.abstracted import SensorPolicy

from cybereason.services.ecosystem import logger


class CRTestCase(BBTestCase):
    pass


class InstallTest(CRTestCase):

    LAB = {
        'endpoint': {
            'class': WindowsHost,
            'boxes': [],
         },
        'repository': {
            'class': LinuxHost,
            'boxes': [],
         },
        'perspective': {
            'class': LinuxHost,
            'boxes': [PerspectiveBox],
         },
        'transparency': {
            'class': LinuxHost,
            'boxes': [TransparencyBox, RegistryBox, PersonalizationBox],
         },
        'download': {
            'class': LinuxHost,
            'boxes': [DownloadBox],
        }
    }

    RLAB = {
        'hosts': {'endpoint': {'class': WindowsHost}},
        'boxes': [PerspectiveBox,
                  TransparencyBox,
                  RegistryBox,
                  PersonalizationBox,
                  10*[SensorBox]]
    }

    address_book = {
        'perspective':
            {'ip': '3.86.19.247', 'username': 'admin@cybereason.com', 'password': 'jPUoWCg8Pok='}
    }

    raddress_book = {
        PerspectiveBox:
            {'ip': '3.86.19.247', 'username': 'admin@cybereason.com', 'password': 'jPUoWCg8Pok='}
    }

    def test_install(self):
        perspective_host = self.lab.hosts['perspective']
        logger.info(f'perspective_host.ip = {perspective_host.ip}')
        perspective = self.lab.boxes[PerspectiveBox.NAME][0]
        logger.info(f'perspective.host.ip = {perspective.host.ip}')

        transparency = self.lab.boxes[TransparencyBox.NAME][0]

        # CYBR-15877 - Add SensorPolicy configuration to SensorPolicy BB to allow Sensor Policy configurations

        sensor_policy = SensorPolicy(server=transparency)
        self.assertRaises(NotImplementedError, sensor_policy.config, None)

        sensor_policy = SensorPolicy(server=perspective)
        sensor_policy.config(None)

        # CYBR-15879 - Add Porxy configuration to Porxy BB to allow Porxy configurations

        # CYBR-15883 - Add to Personaliztion BB the functionality to Download package from Packages Server and Personalize it

        personalization = self.lab.boxes[PersonalizationBox.NAME][0]
        personalization.download(DownloadBox, 'version')
        personalization.personalize()

        # CYBR-15886 - Add functionality to Endpoint Host to download package from the Personalization server

        endpoint = self.lab.hosts['endpoint']
        sensor = SensorBox(endpoint)
        sensor.download(personalization)
        sensor.install_wo_download()
