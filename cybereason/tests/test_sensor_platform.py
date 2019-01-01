"""
"""

from bbtest import WindowsHost, LinuxHost, LocalWindowsHost
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
            'class': LocalWindowsHost,
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
            'class': LocalWindowsHost,
            'boxes': [PersonalizationBox],
        },
    }


    def test_install(self):
        perspective = self.lab.boxes[PerspectiveBox.NAME][0]
        transparency = self.lab.boxes[TransparencyBox.NAME][0]
        endpoint = self.lab.hosts['endpoint']

        # CYBR-15877 - Add SensorPolicy configuration to SensorPolicy BB
        #              to allow Sensor Policy configurations

        sensor_policy = SensorPolicy(server=transparency)
        self.assertRaises(NotImplementedError, sensor_policy.config, None)

        sensor_policy = SensorPolicy(server=perspective)
        sensor_policy.config(None)

        # CYBR-15879 - Add Proxy configuration to Proxy BB to allow Proxy configurations.

        # CYBR-15883 - Add to Personaliztion BB the functionality to
        #              Download package from Packages Server and Personalize it

        personalization = self.lab.boxes[PersonalizationBox.NAME][0]
        artifactory = self.lab.boxes[ArtifactoryBox.NAME][0]
        package_downloaded, personalizer_downloaded = personalization.download(
            artifactory, 'rc-18.1.40', endpoint)
        assert personalization.host.isfile(package_downloaded)
        assert personalization.host.isfile(personalizer_downloaded)

        installer_package_path = personalization.personalize(package_downloaded, personalizer_downloaded, transparency)
        assert personalization.host.isfile(installer_package_path)

        # CYBR-15886 - Add functionality to Endpoint Host to download package from the Personalization server
        sensor = SensorBox(host=endpoint)
        sensor.download(personalization)
        sensor.install_wo_download()

        # Validate
        # self.test_installed_and_running()


    def test_installed_and_running(self):
        endpoint = self.lab.hosts['endpoint']

        # CYBR-15909 - Add functionality to Sensor BB to get Sensor Packages info
        assert endpoint.is_package_installed('Cybereason Sensor')
        # CYBR-15908 - Add functionality to Sensor BB to get Sensor Process Status
        assert endpoint.is_process_running('ActiveConsole.exe')
        assert endpoint.is_process_running('PylumLoader.exe')
        assert endpoint.is_process_running('minionhost.exe')

        # CYBR-15907 - Add functionality to Sensor BB to get Sensor Service Status
        assert endpoint.is_service_running('CybereasonActiveProbe')
