"""
"""

from bbtest import WindowsHost, LinuxHost, LocalHost
from bbtest import BBTestCase

from cybereason.boxes.servers import (TransparencyBox, RegistrationBox, PerspectiveBox, PersonalizationBox,
                                      ArtifactoryBox)
from cybereason.boxes.sensor import SensorBox
from cybereason.services.abstracted import SensorPolicy


class CRTestCase(BBTestCase):
    pass


class InstallTest(CRTestCase):

    LAB = {
        'endpoint': {
            'class': LocalHost,
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
            'boxes': [TransparencyBox],
         },
        'registration': {
            'class': LinuxHost,
            'boxes': [RegistrationBox],
         },
        'download': {
            'class': LinuxHost,
            'boxes': [ArtifactoryBox],
        },
        'local': {
            'class': LocalHost,
            'boxes': [PersonalizationBox],
        },
        # 'file_server': {
        #     'class': BaseHost,
        #     'boxes': [],
        # }
    }

    address_book = {
        'perspective':
            {'ip': '3.86.19.247', 'username': 'admin@cybereason.com', 'password': 'jPUoWCg8Pok='},
        'transparency':
            {'ip': '3.85.179.129'},
        'file_server':
            {'ip': 'cyber-venvs.cyberdomain.local', 'username': 'CYBERDOMAIN\\Automation',
             'password': '$yberAut0Acc3ss', 'root_directory': '\\\\cyber-venvs\\deployments'},
    }

    # FFU

    RLAB = {
        'hosts': {'endpoint': {'class': WindowsHost}},
        'boxes': [PerspectiveBox,
                  TransparencyBox,
                  RegistrationBox,
                  PersonalizationBox,
                  10*[SensorBox]]
    }

    raddress_book = {
        PerspectiveBox:
            {'ip': '3.86.19.247', 'username': 'admin@cybereason.com', 'password': 'jPUoWCg8Pok='}
    }

    # End FFU

    def test_install(self):
        perspective = self.lab.boxes[PerspectiveBox.NAME][0]
        transparency = self.lab.boxes[TransparencyBox.NAME][0]
        endpoint = self.lab.hosts['endpoint']
        # file_server = FileServer(self.lab.hosts['file_server'], self.address_book['file_server']['root_directory'])

        # CYBR-15877 - Add SensorPolicy configuration to SensorPolicy BB to allow Sensor Policy configurations

        sensor_policy = SensorPolicy(server=transparency)
        self.assertRaises(NotImplementedError, sensor_policy.config, None)

        sensor_policy = SensorPolicy(server=perspective)
        sensor_policy.config(None)

        # CYBR-15879 - Add Proxy configuration to Proxy BB to allow Proxy configurations.

        # CYBR-15883 - Add to Personaliztion BB the functionality to Download package from Packages Server and Personalize it

        personalization = self.lab.boxes[PersonalizationBox.NAME][0]
        artifactory = self.lab.boxes[ArtifactoryBox.NAME][0]
        package_downloaded, personalizer_downloaded = personalization.download(artifactory, 'rc-18.1.40', endpoint)
        assert personalization.host.isfile(package_downloaded)
        assert personalization.host.isfile(personalizer_downloaded)

        installer_package_path = personalization.personalize(package_downloaded, personalizer_downloaded, transparency)
        assert personalization.host.isfile(installer_package_path)

        # CYBR-15886 - Add functionality to Endpoint Host to download package from the Personalization server
        sensor = SensorBox(endpoint)
        sensor.download(personalization)
        sensor.install_wo_download()

        # Install

    def test_validate(self):
        endpoint = self.lab.hosts['endpoint']

        # CYBR-15908 - Add functionality to Sensor BB to get Sensor Process Status
        assert endpoint.is_process_running('ActiveConsole.exe'), "Process is not running"
        assert endpoint.is_process_running('PylumLoader.exe'), "Process is not running"
        assert endpoint.is_process_running('minionhost.exe'), "Process is not running"

        # CYBR-15907 - Add functionality to Sensor BB to get Sensor Service Status
        assert endpoint.is_service_running('CybereasonActiveProbe'), "Service is not running"

        # CYBR-15909 - Add functionality to Sensor BB to get Sensor Packages info
        assert endpoint.is_package_installed('Cybereason Sensor'), "Package is not installed"


