"""
"""

from bbtest import BBTestCase
from bbtest import LocalWindowsHost
from cybereason.boxes.sensor import SensorBox
from cybereason.boxes.servers import TransparencyBox, PersonalizationBox, ArtifactoryBox


class InstallTest(BBTestCase):

    LAB = {
        'endpoint': {
            'class': LocalWindowsHost,
            'boxes': [],
         },
        'transparency': {
            'class': LocalWindowsHost,
            'boxes': [TransparencyBox],
         },
        'download': {
            'class': LocalWindowsHost,
            'boxes': [ArtifactoryBox],
        },
        'local': {
            'class': LocalWindowsHost,
            'boxes': [PersonalizationBox],
        },
    }

    def test_install(self):
        """
        TODO
        # CYBR-15877 - Add SensorPolicy configuration to SensorPolicy BB
        #              to allow Sensor Policy configurations

        # CYBR-15879 - Add Proxy configuration to Proxy BB to allow Proxy configurations.

        # CYBR-15883 - Add to Personaliztion BB the functionality to
        #              Download package from Packages Server and Personalize it
        """
        endpoint = self.lab.hosts['endpoint']
        sensor = SensorBox(host=endpoint)
        transparency = self.lab.boxes[TransparencyBox.NAME][0]

        personalization = self.lab.boxes[PersonalizationBox.NAME][0]
        artifactory = self.lab.boxes[ArtifactoryBox.NAME][0]

        tested_version = 'rc-18.1.50' # todo - get tested version from external source
        package_downloaded, personalizer_downloaded = personalization.download(artifactory, tested_version, endpoint)
        assert personalization.host.isfile(package_downloaded)
        assert personalization.host.isfile(personalizer_downloaded)

        installer_package_path = personalization.personalize(package_downloaded, personalizer_downloaded, transparency)
        assert personalization.host.isfile(installer_package_path)

        # CYBR-15886 - Add functionality to Endpoint Host to download package from the Personalization server
        sensor.download(personalization)

        # CYBR-15889 - Add functionality to Endpoint BB to install sensor from local package
        sensor.install_wo_download(installer_package_path)

        # CYBR-15909 - Add functionality to Sensor BB to get Sensor Packages info
        expected_version = sensor.extract_version_from_file(installer_package_path)
        assert endpoint.is_version_installed('Cybereason Sensor', expected_version), \
            f"Cybereason Sensor {expected_version} is not installed"

        # CYBR-15908 - Add functionality to Sensor BB to get Sensor Process Status
        assert endpoint.is_process_running('ActiveConsole.exe'), "ActiveConsole.exe is not running"
        assert endpoint.is_process_running('PylumLoader.exe'), "PylumLoader.exe is not running"
        assert endpoint.is_process_running('minionhost.exe'), "minionhost.exe is not running"

        # CYBR-15907 - Add functionality to Sensor BB to get Sensor Service Status
        assert endpoint.is_service_running('CybereasonActiveProbe'), "CybereasonActiveProbe Service is not running"

        # CYBR-15936 - Add functionality to Sensor BB to get PylumId
        assert sensor.calc_pylumid() == sensor.open_key('Identifier'), "PylumId not exists or incorrect"
