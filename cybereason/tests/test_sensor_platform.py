"""
"""
from bbtest import BBTestCase, WindowsHost, LinuxHost, os, DebianHost
from bbtest import LocalWindowsHost
from cybereason.boxes.sensor import SensorBox
from cybereason.boxes.servers import TransparencyBox, PersonalizationBox, ArtifactoryBox


class InstallTest(BBTestCase):

    LAB = {
        'endpoint': {
            'class': DebianHost,
            'boxes': [PersonalizationBox],
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
            'boxes': [],
        },
    }

    address_book = {'endpoint': {'ip': '172.16.30.22', 'auth': ['root', 'Password1']}}

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

        tested_version = 'rc-18.1.50'  # todo - get tested version from external source
        package_downloaded, personalizer_downloaded = personalization.download(artifactory, tested_version, endpoint)
        assert personalization.host.isfile(package_downloaded)
        assert personalization.host.isfile(personalizer_downloaded)

        installer_package_path = personalization.personalize(package_downloaded, personalizer_downloaded, transparency)
        assert personalization.host.isfile(installer_package_path)

        # CYBR-15886 - Add functionality to Endpoint Host to download package from the Personalization server
        installer_path_in_local = personalization.host.get(installer_package_path, os.getcwd())
        installer_path_in_endpoint = endpoint.put(installer_path_in_local,
                                                  installer_path_in_local.replace('\\', '/').split('/')[-1])
        assert endpoint.isfile(installer_path_in_endpoint)

        # CYBR-15889 - Add functionality to Endpoint BB to install sensor from local package
        sensor.install_wo_download(installer_path_in_endpoint)

        # CYBR-15909 - Add functionality to Sensor BB to get Sensor Packages info
        assert sensor.get_version() == sensor.get_installer_version(installer_package_path)

        # CYBR-15908 - Add functionality to Sensor BB to get Sensor Process Status
        assert sensor.is_cr_processes_running()

        assert endpoint.is_process_running('ActiveConsole.exe')
        assert endpoint.is_process_running('PylumLoader.exe')
        assert endpoint.is_process_running('minionhost.exe')

        # CYBR-15907 - Add functionality to Sensor BB to get Sensor Service Status
        assert endpoint.is_service_running('CybereasonActiveProbe')

        # CYBR-15936 - Add functionality to Sensor BB to get PylumId
        assert sensor.calc_pylumid() == sensor.open_key('Identifier')
