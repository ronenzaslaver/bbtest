"""
Hosts in the network.
"""
import logging
import os
import platform
import socket
import subprocess
import shutil
import tempfile

try:
    from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumKey, QueryValueEx
except Exception:
    pass

from ftplib import FTP
import rpyc
import glob

import psutil
from psutil import NoSuchProcess

from bbtest import target


logger = logging.getLogger('bblog')


class BaseHost(object):
    """"A base host class

    :param SEP: The path separator character
    :type SEP: str
    """

    SEP = '/'

    def __init__(self, *args, **kwargs):
        super().__init__()
        try:
            self.ROOT_PATH = self.ROOT_PATH
        except AttributeError:
            self.ROOT_PATH = tempfile.gettempdir()

    def install(self):
        """ install host for bbtest

        We separate install from init so we can create an install hosts in different order.
        """
        pass

    def uninstall(self):
        """ the opposite of install,  uninstall bbtest from host """
        pass

    def clean(self):
        """ Restore host to its original installed state """
        pass

    @property
    def os(self):
        raise NotImplementedError('Missing method implementation')

    @property
    def bit(self):
        raise NotImplementedError('Missing method implementation')

    @property
    def name(self):
        raise NotImplementedError('Missing method implementation')

    @property
    def package_type(self):
        raise NotImplementedError('Non Windows OS')

    def isfile(self, path):
        raise NotImplementedError('Missing method implementation')

    def rmtree(self, path, ignore_errors=True, onerror=None):
        raise NotImplementedError('Missing method implementation')

    def rmfile(self, path):
        raise NotImplementedError('Missing method implementation')

    def run_python2(self, *args, **kwargs):
        """Call run command with python2 as the process"""
        raise NotImplementedError('Missing method implementation')

    def join(self, *args):
        return self.SEP.join(args)


class LocalHost(BaseHost):
    """Suppose to be an os-agnostic local host."""
    ip = '127.0.0.1'

    @property
    def os(self):
        """Returns a lower case string identifying the OS"""
        return platform.platform().lower()

    @property
    def package_type(self):
        if 'win' in self.os:
            return 'msi'
        elif 'ubuntu' in self.os:
            return 'deb'
        raise NotImplementedError('Missing method implementation')

    @property
    def bit(self):
        return platform.machine()[-2:]

    @property
    def name(self):
        return socket.gethostname()

    def run(self, *args, **kwargs):
        logger.debug(f'{self.__class__.__name__} run command: {args} {kwargs}')
        output = target.run(*args, **kwargs)
        logger.debug(f'{self.__class__.__name__} run raw stdout: {output}')
        parsed_output = [] if output == b'' else output.decode('utf-8').splitlines()
        logger.debug(f'{self.__class__.__name__} run parsed stdout: {parsed_output}')
        return parsed_output

    @staticmethod
    def put(local, remote):
        return shutil.copyfile(local, remote)

    @staticmethod
    def get(remote, local):
        return shutil.copyfile(remote, local)

    @staticmethod
    def mkdtemp(**kwargs):
        """ same args as tempfile.mkdtemp """
        return tempfile.mkdtemp(**kwargs)

    @staticmethod
    def rmtree(path, ignore_errors=True, onerror=None):
        return shutil.rmtree(path, ignore_errors, onerror)

    @staticmethod
    def rmfile(path):
        try:
            os.remove(path)
        except OSError:
            pass

    @staticmethod
    def rmfiles(path):
        logger.debug(f"rmfiles with '{path}'")
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    LocalHost.rmtree(os.path.join(root, dir))
        except OSError:
            pass

    def isfile(self, path):
        return os.path.isfile(path)

    @staticmethod
    def is_process_running(process_name):
        for process in psutil.process_iter():
            if process.name() == process_name:
                return True
        return False

    @staticmethod
    def open_key(parent_key, key):
        cybereason_key = OpenKey(HKEY_LOCAL_MACHINE, parent_key)
        return QueryValueEx(cybereason_key, key)[0]


class LocalWindowsHost(LocalHost):

    """A collection of windows utilities and validators """
    ROOT_PATH = 'c:\\temp'
    package_type = 'msi'

    @staticmethod
    def is_version_installed(name, version):
        products = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
        try:
            i = 0
            while True:
                product_key_name = EnumKey(products, i)
                product_values = OpenKey(products, product_key_name)
                try:
                    if QueryValueEx(product_values, 'DisplayName')[0] == name:
                        return QueryValueEx(product_values, 'DisplayVersion')[0] == version
                except FileNotFoundError:
                    # product has no 'DisplayName' attribute
                    pass
                i = i+1
        except WindowsError:
            return False

    def run_python2(self, *args_in, **kwargs):
        args = ['py', '-2']
        args.extend(args_in)
        return self.run(*args, **kwargs)

    @staticmethod
    def is_service_running(service_name):
        try:
            return psutil.win_service_get(service_name).status() == 'running'
        except NoSuchProcess:
            return False

    def get_active_macs(self):
        """
        :return: list of MACs of all active NICs sorted by DeviceID
        """
        args = ['powershell.exe']
        args.append('Get-WmiObject win32_networkadapter | '
                    'Where-Object -Property NetConnectionStatus -eq -Value "2" | '
                    'Sort-Object -Property DeviceId | '
                    'Select-Object -ExpandProperty MACAddress')
        return self.run(*args)


class LocalLinuxHost(LocalHost):

    ROOT_PATH = '/tmp'

    def run_python2(self, *args_in, **kwargs):
        args = ['python2']
        args.extend(args_in)
        return self.run(*args, **kwargs)


class RemoteHost(BaseHost):
    """A remote host using RPyC
    """

    @property
    def os(self):
        return self.modules.bbtest.LocalHost().os

    @property
    def bit(self):
        return self.modules.bbtest.LocalHost().bit

    @property
    def package_type(self):
        return self.modules.bbtest.LocalHost().package_type

    @property
    def name(self):
        return self.modules.bbtest.LocalHost().name

    def __init__(self, ip=None, auth=None):
        """ Initialise remote host - open FTP and rpyc connections.

        :param ip:
        :param auth:
        """
        super().__init__()
        self.ip = str(ip)
        self.auth = auth
        try:
            self.ftp = FTP(ip)
            if auth:
                self.ftp.login(auth[0], auth[1])
            else:
                # Assume anonymous
                self.ftp.login()
        except Exception as e:
            raise ConnectionError(f'Failed to connect to FTP server on host {ip} - {e}')
        try:
            self._rpyc = rpyc.classic.connect(self.ip)
        except Exception as e:
            raise ConnectionError(f'Failed to connect to RPyC server on host {ip} - {e}')
        self.modules = self._rpyc.modules

    def install(self, bbtest_version=None):
        """ Install bbtest package on remote host.

        :param bbtest_version: bbtest version to install.
        """
        super().install()
        root_dir = os.path.dirname(os.path.dirname(os.path.join(os.path.dirname(__file__), 'src')))
        dist_dir = os.path.join(root_dir, 'dist')
        if not bbtest_version:
            def _extract_version(f):
                return float(f.split('-')[1].split('.tar.gz')[0])
            bbtest_packages = glob.glob(os.path.join(dist_dir, 'bbtest-*.tar.gz'))
            try:
                bbtest_package = max(bbtest_packages, key=_extract_version)
            except Exception as e:
                raise Exception(f'Failed to find bbtest package - {e}')
        bbtest_remote = self.put(bbtest_package, bbtest_package.replace('\\', '/').split('/')[-1])
        args = ['python', '-m', 'pip', 'install', '-U', bbtest_remote]
        self.modules.subprocess.run(' '.join(args), shell=True, stdout=subprocess.PIPE)

    def put(self, local, remote):
        ftp_remote = remote.replace(self.ROOT_PATH, '').replace('\\', '/').split('/', 1)[-1]
        self.ftp.storbinary(f'STOR {ftp_remote}', open(local, 'rb'))
        return os.path.join(self.ROOT_PATH, ftp_remote).replace('\\', '/')

    def get(self, remote, local):
        ftp_remote = remote.replace('\\', '/').replace(self.ROOT_PATH, '')
        # ftp_remote = remote.replace('\\', '/').replace(self.root_path, '').split('/', 1)[-1]
        self.ftp.retrbinary(f'RETR {ftp_remote}', open(local, 'wb').write)
        return os.path.join(self.ROOT_PATH, ftp_remote).replace('\\', '/')

    def run(self, *args, **kwargs):
        logger.debug(f'{self.__class__.__name__} run command: {args} {kwargs}')
        output = self.modules.bbtest.target.run(*args, **kwargs)
        logger.debug(f'{self.__class__.__name__} run raw stdout: {output}')
        parsed_output = [] if output == b'' else output.decode('utf-8').splitlines()
        logger.debug(f'{self.__class__.__name__} run parsed stdout: {parsed_output}')
        return parsed_output

    def mkdtemp(self, **kwargs):
        """ same args as tempfile.mkdtemp """
        if 'dir' not in kwargs:
            kwargs['dir'] = self.ROOT_PATH
        return self.modules.bbtest.LocalHost.mkdtemp(**kwargs)

    def rmtree(self, *args, **kwargs):
        return self.modules.bbtest.LocalHost.rmtree(*args, **kwargs)

    def rmfile(self, path):
        return self.modules.bbtest.LocalHost.rmfile(path)

    def is_process_running(self, process):
        return self.modules.bbtest.LocalHost.is_process_running(process)


class WindowsHost(RemoteHost):
    """ A remote windows host """
    ROOT_PATH = 'c:\\temp'

    def __init__(self, ip="localhost", auth=("user", "pass")):
        super().__init__(ip, auth)

    def is_version_installed(self, name, version):
        return self.modules.bbtest.LocalWindowsHost.is_version_installed(name, version)

    def rmfiles(self, name):
        return self.modules.bbtest.LocalHost.rmfiles(name)

    def isfile(self, path):
        return self.modules.bbtest.LocalWindowsHost.isfile(path)

    def open_key(self, parent_key, key):
        return self.modules.bbtest.LocalHost.open_key(parent_key, key)

    def get_active_macs(self):
        return self.modules.bbtest.LocalWindowsHost().get_active_macs()

    def is_service_running(self, service):
        return self.modules.bbtest.LocalWindowsHost.is_service_running(service)


class LinuxHost(RemoteHost):

    ROOT_PATH = '/tmp'

    def run(self, *args, **kwargs):
        return super().run(' '.join(args), **kwargs)

    def is_service_running(self, service):
        raise NotImplementedError('Missing method implementation')

    def is_version_installed(self, name, version):
        raise NotImplementedError('Missing method implementation')


class OSXHost(LinuxHost):
    pass
