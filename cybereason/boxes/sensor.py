import re
from winreg import QueryValueEx, OpenKey, HKEY_LOCAL_MACHINE

from cybereason.services.ecosystem import logger
from . import CRBox


class SensorBox(CRBox):

    def install(self, personalization):
        self.download(personalization)
        self.install_wo_download()

    def download(self, personalization):
        logger.info(f'download from personalization server {personalization}')

    def install_wo_download(self, installer_path):
        logger.info('install sensor on endpoint')
        install_command = ['/install', '/quiet', '/norestart']
        self.host.run(installer_path, *install_command)

    @staticmethod
    def open_key(key_name):
        cybereason_key = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Cybereason\ActiveProbe')
        # TODO find a better more abstract way for querying the registry
        return QueryValueEx(cybereason_key, key_name)[0]

    def calc_pylumid(self):
        separator = '_'
        prefix = 'Py10:PylumClient'
        organization = self.open_key('server.organization')
        host_name = self.host.name
        machine_mac_address = self.host.get_active_macs()[0].replace(":", "")
        pylumid = separator.join([prefix, organization, host_name, machine_mac_address])
        return pylumid.upper()

    @staticmethod
    def extract_version_from_file(file_name):
        file_name = file_name.replace('\\', '/').split('/')[-1]
        pattern = r'(cybereason-sensor-|ActiveProbe_|Cybereason(ActiveProbe|Console|Sensor)(32|64)_)' \
                  r'(?P<version>\d+[_,.]\d+[_,.]\d+[_,.]\d+)'
        match = re.match(pattern, file_name)
        if match:
            return match.groupdict()['version'].replace('_', '.')
        else:
            raise RuntimeError('Cannot extract version from file name')


class NgavBox(CRBox):
    pass


class PowershellBox(CRBox):
    pass
