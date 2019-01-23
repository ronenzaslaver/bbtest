import os
import tarfile

from artifactory import ArtifactoryPath

from bbtest import BaseHost, WindowsHost, LinuxHost, OsxHost, LocalHost
from cybereason.services.ecosystem import logger

from . import CRBox

ARTIFACTORY_SENSOR_REPO_URL = 'http://artifactory01:8081/artifactory/sensor/cybereason'


class CRServerBox(CRBox):

    def download_file(self, file_path):
        dest_file_path = self.host.SEP.join([self.path, os.path.basename(file_path)])
        self.host.download_file(file_path, dest_file_path)
        return dest_file_path


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
    Run python 2.7 with 'pip install protobuf' and 'pip install google'
    Copy files to a drive shared with EPs under test (e.g. \\cyberdev\\data\\ep_automation_shared)
    """

    def __init__(self, host, name=None):
        super().__init__(host, name=name)
        # if not issubclass(type(self.host), LocalHost):
        #     raise NotImplementedError(f'Box {self.NAME} is not support on host type: {self.host}')

    def download(self, download_server, version, endpoint):
        """ Download installer package and personalizer from download server
        :param download_server:
        :param version:
        :param endpoint:
        :type endpoint: BaseHost
        :return:
        """

        if 'windows' in endpoint.os.lower():
            os_to_prefix = 'CybereasonSensor' + endpoint.bit
        if "linux" in endpoint.os.lower():
            os_to_prefix = 'cybereason-sensor-'
        if "mac" in endpoint.os.lower():  # todo get correct 'mac' string
            os_to_prefix = 'ActiveProbe_'

        if type(download_server) == ArtifactoryBox:
            # download installer package
            package_artifact_path = self._find_artifact_url(
                f'{ARTIFACTORY_SENSOR_REPO_URL}/{version}/{endpoint.package_type}', os_to_prefix)
            package_dest_file_path = self.download_file(package_artifact_path)

            # download personalizer package
            personalizer_artifact_path = self._find_artifact_url(
                f'{ARTIFACTORY_SENSOR_REPO_URL}/{version}/personalization', "personalizer-")
            personalizer_dest_file_path = self.download_file(personalizer_artifact_path)
        else:
            raise NotImplementedError(f'Personalization does not support download from {download_server.NAME} server')

        return package_dest_file_path, personalizer_dest_file_path

    def personalize(self, installer_package_path, personalizer_tar, registration_or_transparency):
        """ Personalize the installer package
        User must provide Transparency or Registration.
        :todo in the future we'll need to add support to get them by logic from LAB object.
        :todo support kwargs param for all personalization features/flags
        :param installer_package_path:
        :param personalizer_tar:
        :param registration:
        :param transparency:
        :return:
        """

        logger.info(f'Untar the personalizer tool')
        self.host.untar_file(personalizer_tar)

        # personalize the installer package
        if type(registration_or_transparency) is RegistrationBox:
            server_flag = '-ss'
            port_flag = '-sp'
        else:
            server_flag = '-s'
            port_flag = '-p'

        personalization_script_path = self.host.SEP.join([self.path, 'personalizePackage.py'])
        personalization_command = [personalization_script_path, server_flag, registration_or_transparency.host.ip,
                                   port_flag, '8443', '-org', 'cybereason', '-f', installer_package_path,
                                   '-o', self.path]

        personalization_output = self.host.run_python2(personalization_command)
        personalization_file_name = personalization_output[-1].replace('\\', '/').split('/')[-1]
        return self.host.SEP.join([self.path, personalization_file_name])

    @staticmethod
    def _find_artifact(latest_build_path, package_prefix):
        for artifact_path in latest_build_path:
            artifact_file_name = os.path.basename(artifact_path)
            if artifact_file_name.startswith(package_prefix):
                return artifact_path

    @staticmethod
    def _extract_build_number(f):
        return int(os.path.basename(f))

    def _find_artifact_url(self, artifactory_url, file_prefix):
        branch_builds = ArtifactoryPath(artifactory_url)
        latest_build_path = max(branch_builds, key=self._extract_build_number)
        package_artifact_path = self._find_artifact(latest_build_path, file_prefix)
        return package_artifact_path


class ProxyBox(CRServerBox):
    pass


class DownloadBox(CRServerBox):
    pass


class IreleaseBox(DownloadBox):
    pass


class ArtifactoryBox(DownloadBox):
    pass


# class SharedFolderBox(BB):
