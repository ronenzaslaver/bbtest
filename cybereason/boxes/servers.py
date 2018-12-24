
from cybereason.services.ecosystem import logger

from cybereason.boxes.boxes import CRBox


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

    def download(self, download_server, version):
        if type(download_server) == IreleaseBox:
            logger.info(f'download personalizer and installer version {version} from {download_server}')
        else:
            raise NotImplementedError(f'Personalization does not support download from {download_server.NAME} server')

    def personalize(self):
        logger.info(f'personalize')


class ProxyBox(CRServerBox):
    pass


class DownloadBox(CRServerBox):
    pass


class IreleaseBox(DownloadBox):
    pass


class ArtifactoryBox(DownloadBox):
    pass
