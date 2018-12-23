
from cybereason.services.ecosystem import logger

from cybereason.boxes.boxes import CRBox


class CRServerBox(CRBox):
    pass


class PerspectiveBox(CRServerBox):
    NAME = 'perspective'


class TransparencyBox(CRServerBox):
    NAME = 'transparency'


class RegistryBox(CRServerBox):
    NAME = 'registry'


class PersonalizationBox(CRServerBox):

    def download(self, download_server, version):
        logger.info(f'download personalizer and installer version {version} from {download_server}')

    def personalize(self):
        logger.info(f'personalize')


class ProxyBox(CRServerBox):
    pass


class DownloadBox(CRServerBox):
    pass
