import re

from bbtest import WindowsHost, LocalWindowsHost, FedoraHost, LocalFedoraHost, LocalDebianHost, DebianHost, OsxHost
from cybereason.services.ecosystem import logger
from . import CRBox


class LocalOsxHost(object):
    pass


class SensorBox(CRBox):

    def __init__(self, host, name=None):
        super().__init__(host, name)
        host_2_sensor = {
            WindowsHost: WindowsSensorBox, LocalWindowsHost: WindowsSensorBox,
            FedoraHost: FedoraSensorBox, LocalFedoraHost: FedoraSensorBox,
            DebianHost: DebianSensorBox, LocalDebianHost: DebianSensorBox,
            OsxHost: OsxSensorBox, LocalOsxHost: OsxSensorBox
        }
        self.__class__ = host_2_sensor[type(host)]


    def install(self, personalization):
        self.download(personalization)
        self.install_wo_download()

    def download(self, personalization):
        logger.info(f'download from personalization server {personalization}')

    def open_key(self, key_name):
        cybereason_key = r'SOFTWARE\Cybereason\ActiveProbe'
        # TODO find a better more abstract way for querying the registry
        return self.host.open_key(cybereason_key, key_name)

    def calc_pylumid(self):
        separator = '_'
        prefix = 'Py10:PylumClient'
        organization = self.open_key('server.organization')
        host_name = self.host.name
        machine_mac_address = self.host.get_active_macs()[0].replace(":", "")
        pylumid = separator.join([prefix, organization, host_name, machine_mac_address])
        return pylumid.upper()

    @staticmethod
    def get_installer_version(file_name):
        file_name = file_name.replace('\\', '/').split('/')[-1]
        pattern = r'(cybereason-sensor-|ActiveProbe_|Cybereason(ActiveProbe|Console|Sensor)(32|64)_)' \
                  r'(?P<version>\d+[_,.]\d+[_,.]\d+[_,.]\d+)'
        match = re.match(pattern, file_name)
        if match:
            return match.groupdict()['version'].replace('_', '.')
        else:
            raise RuntimeError('Cannot extract version from file name')

    def is_processes_running(self, processes):
        success = True
        for process in processes:
            if not self.host.is_process_running(process):
                logger.warning(f'Process {process} not found')
                success = False
        return success


class WindowsSensorBox(SensorBox):

    def install_wo_download(self, installer_path):
        logger.info('install sensor on endpoint')
        self.host.run([f'{installer_path}/install', '/quiet', '/norestart'])


class FedoraSensorBox(SensorBox):
    pass


class DebianSensorBox(SensorBox):

    def install_wo_download(self, installer_path):
        logger.info('install sensor on endpoint')
        self.host.run(['sudo', 'dpkg', '-i', f'{installer_path}'])

    def get_version(self):
        try:
            command = 'dpkg --status cybereason-sensor | sed --quiet --expression "s/^Version: //p"'
            return self.host.run(command, shell=True)[0]
        except Exception as e:
            raise RuntimeError(f'Failed to get sensor version - {e}')

    def is_cr_processes_running(self):
        processes = ['Cybereason-serv']
        return super(DebianSensorBox, self).is_processes_running(processes)


class OsxSensorBox(SensorBox):
    pass


class NgavBox(CRBox):
    pass


class PowershellBox(CRBox):
    pass
