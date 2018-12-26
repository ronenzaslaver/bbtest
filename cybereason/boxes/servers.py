import os

from artifactory import ArtifactoryPath

from bbtest import BaseHost, WindowsHost, LinuxHost, OSXHost
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
            # find the artifact url
            branch_builds = ArtifactoryPath(f'{ARTIFACTORY_SENSOR_REPO_URL}/{version}/{endpoint.PACKAGE_TYPE}')
            latest_build_path = max(branch_builds, key=self._extract_build_number)
            package_prefix = os_to_prefix[endpoint.OS]
            artifact_path = self._find_artifact(latest_build_path, package_prefix)

            # download the artifact
            logger.info(f'Downloading package from: {artifact_path}')
            package_dest_file_path = self.path + endpoint._SEP + os.path.basename(artifact_path)
            with artifact_path.open() as fd:
                with open(package_dest_file_path, "wb") as out:
                    out.write(fd.read())
            logger.info(f'Downloaded file path on disk: {package_dest_file_path}')
        else:
            raise NotImplementedError(f'Personalization does not support download from {download_server.NAME} server')

        return package_dest_file_path

    def personalize(self):
        logger.info(f'personalize')

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
