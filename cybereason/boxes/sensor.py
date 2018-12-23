
from cybereason.services.ecosystem import logger

from cybereason.boxes.boxes import CRBox


class SensorBox(CRBox):

    def install(self, personalization):
        self.download(personalization)
        self.install_wo_download()

    def download(self, personalization):
        logger.info(f'download from personalization server {personalization}')

    def install_wo_download(self):
        logger.info('install sensor on endpoint')


class NgavBox(CRBox):
    pass


class PowershellBox(CRBox):
    pass
