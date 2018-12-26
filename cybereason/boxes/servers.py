import os
import tarfile

from artifactory import ArtifactoryPath

from bbtest import BaseHost, WindowsHost, LinuxHost, OSXHost, LocalHost
from cybereason.services.ecosystem import logger

from . import CRBox

ARTIFACTORY_SENSOR_REPO_URL = 'http://artifactory01:8081/artifactory/sensor/cybereason'


class CRServerBox(CRBox):
    pass


class PerspectiveBox(CRServerBox):
    NAME = 'perspective'


class TransparencyBox(CRServerBox):
    NAME = 'transparency'


class RegistrationBox(CRServerBox):
    NAME = 'registry'


class PersonalizationBox(CRServerBox):
    """
    Can run on any machine that can:
    Access the download server
    Untar the personalizer script
    Run python 2.7
    Send files to other machines
    """

    def __init__(self, host, name=None):
        super().__init__(host, name=name)
        if type(self.host) is not LocalHost:
            raise NotImplementedError(f'Box {self.NAME} is not support on host type: {self.host}')

    def download(self, download_server, version, endpoint):
        """

        :param download_server:
        :param version:
        :param endpoint:
        :type endpoint: BaseHost
        :return:
        """

        os_to_prefix = {WindowsHost.OS: 'CybereasonSensor' + endpoint.BIT,
                        LinuxHost.OS: 'cybereason-sensor-',
                        OSXHost.OS: 'ActiveProbe_'}

        if type(download_server) == ArtifactoryBox:
            # find installer package artifact url
            branch_builds = ArtifactoryPath(f'{ARTIFACTORY_SENSOR_REPO_URL}/{version}/{endpoint.PACKAGE_TYPE}')
            latest_build_path = max(branch_builds, key=self._extract_build_number)
            package_prefix = os_to_prefix[endpoint.OS]
            package_artifact_path = self._find_artifact(latest_build_path, package_prefix)

            # download installer package artifact
            logger.info(f'Downloading personalizer from: {package_artifact_path}')
            package_dest_file_path = self.path + endpoint._SEP + os.path.basename(package_artifact_path)
            with package_artifact_path.open() as fd:
                with open(package_dest_file_path, "wb") as out:
                    out.write(fd.read())
            logger.info(f'Downloaded file path on disk: {package_dest_file_path}')

            # find personalizer artifact url
            personalizer_builds = ArtifactoryPath(f'{ARTIFACTORY_SENSOR_REPO_URL}/{version}/personalization')
            latest_build_path = max(personalizer_builds, key=self._extract_build_number)
            personalizer_artifact_path = self._find_artifact(latest_build_path, "personalizer-")

            # download personalizer artifact
            logger.info(f'Downloading personalizer from: {personalizer_artifact_path}')
            personalizer_dest_file_path = self.path + endpoint._SEP + os.path.basename(personalizer_artifact_path)
            with personalizer_artifact_path.open() as fd:
                with open(personalizer_dest_file_path, "wb") as out:
                    out.write(fd.read())
            logger.info(f'Downloaded file path on disk: {personalizer_dest_file_path}')

        else:
            raise NotImplementedError(f'Personalization does not support download from {download_server.NAME} server')

        return package_dest_file_path, personalizer_dest_file_path

    def personalize(self, installer_package, personalizer_tar, registration_or_transparency, **kwargs):
        """
        User must provide Transparency or Registration.
        in the future we'll need to add support to get them by logic from LAB object.
        :param installer_package:
        :param personalizer_tar:
        :param registration:
        :param transparency:
        :param kwargs:
        :return:
        """

        # untar personalizer tool
        logger.info(f'Untar the personalizer tool')
        if personalizer_tar.endswith('tar.gz'):
            tar = tarfile.open(personalizer_tar, "r:gz")
            tar.extractall(path=os.path.dirname(personalizer_tar))
            tar.close()
        else:
            # todo add the actual file extension to exception
            raise NotImplementedError('personalizer file extension is not supported')

        # personalize the installer package
        if type(registration_or_transparency) is RegistrationBox:
            server_flag = '-ss'
            port_flag = '-sp'
        else:
            server_flag = '-s'
            port_flag = '-p'


        personalization_script_path = os.path.dirname(personalizer_tar) + self.host._SEP + 'personalizePackage.py'
        personalization_command = [personalization_script_path, server_flag, registration_or_transparency.host.ip, port_flag, '8443',
                                   '-org', 'cybereason', '-c', 'True', '-f', installer_package, '-u', os.path.dirname(personalizer_tar)]

        result = self.host.run('C:\\python27\python.exe', *personalization_command)



    @staticmethod
    def _find_artifact(latest_build_path, package_prefix):
        for artifact_path in latest_build_path:
            artifact_file_name = os.path.basename(artifact_path)
            if artifact_file_name.startswith(package_prefix):
                return artifact_path

    @staticmethod
    def _extract_build_number(f):
        return int(os.path.basename(f))

class ProxyBox(CRServerBox):
    pass


class DownloadBox(CRServerBox):
    pass


class IreleaseBox(DownloadBox):
    pass


class ArtifactoryBox(DownloadBox):
    pass
