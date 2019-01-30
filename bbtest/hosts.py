"""
Hosts in the network.
"""
import logging
import os
import platform
import socket
import subprocess
import shutil
import tarfile
import tempfile
import time
from ftplib import FTP
import rpyc
import glob
import psutil
from psutil import NoSuchProcess
try:
    from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumKey, QueryValueEx
except Exception:
    pass

from bbtest import target

SYNC_REQUEST_TIMEOUT = 60

logger = logging.getLogger('bblog')


class BaseHost(object):
    """"A base host class

    :param SEP: The path separator character
    :type SEP: str
    """

    SEP = '/'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.root_path = getattr(self, 'ROOT_PATH', tempfile.gettempdir())

    @property
    def os(self):
        """Returns a lower case string identifying the OS"""
        return self.target.os()

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
    def bit(self):
        raise NotImplementedError('Missing method implementation')

    @property
    def name(self):
        raise NotImplementedError('Missing method implementation')

    @property
    def package_type(self):
        # TODO - define by os type and not by class name
        host_2_package_type = {
            WindowsHost: 'msi',
            LocalWindowsHost: 'msi',
            FedoraHost: 'rpm',
            LocalFedoraHost: 'rpm',
            DebianHost: 'deb',
            LocalDebianHost: 'deb',
            OSXHost: 'pkg',
            LocalOSXHost: 'pkg'
        }
        return host_2_package_type[self.__class__]

    @property
    def is_winodws(self):
        return 'windows' in self.os

    @property
    def is_linux(self):
        return 'linux' in self.os

    def isfile(self, path):
        raise NotImplementedError('Missing method implementation')

    def rmtree(self, path, ignore_errors=True, onerror=None):
        raise NotImplementedError('Missing method implementation')

    def rmfile(self, path):
        raise NotImplementedError('Missing method implementation')

    def run(self, args, **kwargs):
        logger.debug(f'{self.__class__.__name__} run command: {args} {kwargs}')
        shutils_kwargs = {k: v for k, v in kwargs.items() if k not in rpyc.core.protocol.DEFAULT_CONFIG}
        output = self.target.run(args, **shutils_kwargs)
        if output.returncode > 0:
            raise subprocess.SubprocessError(f'subprocess run "{args} {kwargs}" failed on target\n'
                                             f'stdout = {output.stdout}\n'
                                             f'stderr = {output.stderr}')
        logger.debug(f'{self.__class__.__name__} run raw stdout: {output.stdout}')
        parsed_output = [] if output.stdout == b'' else output.stdout.decode('utf-8').splitlines()
        logger.debug(f'{self.__class__.__name__} run parsed stdout: {parsed_output}')
        return parsed_output

    def run_python2(self, args_in, **kwargs):
        return self._run_python(2, args_in, **kwargs)

    def run_python3(self, args_in, **kwargs):
        return self._run_python(3, args_in, **kwargs)

    def _run_python(self, version, args_in, **kwargs):
        args = ['py', '-' + str(version)] if self.is_winodws else ['python' + str(version)]
        args.extend(args_in)
        return self.run(args, **kwargs)

    def join(self, *args):
        return self.SEP.join(args)

    def download_file(self, src_path, dst_path):
        return self.target.download_file(src_path, dst_path)


class LocalHost(BaseHost):
    """Suppose to be an os-agnostic local host."""
    ip = '127.0.0.1'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.target = target

    @property
    def bit(self):
        return platform.machine()[-2:]

    @property
    def name(self):
        return socket.gethostname()

    def put(self, local, remote):
        """ Put file on target host relative to root path. """
        return shutil.copyfile(local, self._relative_remote(remote))

    def get(self, remote, local):
        """ Get file from target host relative to root path. """
        return shutil.copyfile(self._relative_remote(remote), local)

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
    def is_process_running(proc_name, timeout=1):
        for _ in range(0, timeout):
            for proc in psutil.process_iter():
                if proc.name() == proc_name:
                    return True
            time.sleep(1)
        return False

    @staticmethod
    def open_key(parent_key, key):
        parent = OpenKey(HKEY_LOCAL_MACHINE, parent_key)
        return QueryValueEx(parent, key)[0]

    @staticmethod
    def untar_file(path):
        if path.endswith('tar.gz'):
            tar = tarfile.open(path, "r:gz")
            tar.extractall(path=os.path.dirname(path))
            tar.close()
        else:
            # todo add the actual file extension to exception
            raise NotImplementedError('File extension is not supported')

    def _relative_remote(self, remote):
        return os.path.join(self.root_path, remote.replace('\\', '/').replace(self.root_path, ''))


class LocalWindowsHost(LocalHost):

    """A collection of windows utilities and validators """
    ROOT_PATH = 'c:/temp'

    @staticmethod
    def get_package_version(package_name):
        products = OpenKey(HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall')
        try:
            i = 0
            while True:
                product_key_name = EnumKey(products, i)
                product_values = OpenKey(products, product_key_name)
                try:
                    if QueryValueEx(product_values, 'DisplayName')[0] == package_name:
                        return QueryValueEx(product_values, 'DisplayVersion')[0]
                except FileNotFoundError:
                    # product has no 'DisplayName' attribute
                    pass
                i = i+1
        except WindowsError:
            raise RuntimeError('Cybereason version not found')

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
        return self.run(args)


class LocalLinuxHost(LocalHost):

    ROOT_PATH = '/tmp'

    @staticmethod
    def is_service_running(service_name):
        return True if os.system(f'service {service_name} status') == 0 else False


class LocalFedoraHost(LocalLinuxHost):
    pass


class LocalDebianHost(LocalLinuxHost):
    pass


class LocalOSXHost(LocalHost):

    def is_service_running(self, service_name):
        command = f'sudo launchctl list | awk \'$3=="{service_name}" {{ print $2 }}\''
        if self.run(command, shell=True)[0] == '0':
            return True
        else:
            return False


class RemoteHost(BaseHost):
    """A remote host using RPyC
    """

    @property
    def bit(self):
        return self.modules.bbtest.LocalHost().bit

    @property
    def name(self):
        return self.modules.bbtest.LocalHost().name

    def __init__(self, ip=None, auth=None, *args, **kwargs):
        """ Initialise remote host - open FTP and rpyc connections.

        :param ip:
        :param auth:
        """
        super().__init__(*args, **kwargs)
        self.ip = str(ip)
        self.auth = auth
        try:
            self.ftp = FTP(self.ip)
            if auth:
                self.ftp.login(auth[0], auth[1])
            else:
                # Assume anonymous
                self.ftp.login()
        except Exception as e:
            raise ConnectionError(f'Failed to connect to FTP server on host {ip} - {e}')
        try:
            rpyc.core.protocol.DEFAULT_CONFIG['sync_request_timeout'] = SYNC_REQUEST_TIMEOUT
            self._rpyc = rpyc.classic.connect(self.ip)
        except Exception as e:
            raise ConnectionError(f'Failed to connect to RPyC server on host {ip} - {e}')
        self.modules = self._rpyc.modules
        self.target = self.modules.bbtest.target

    def install(self, bbtest_version=None):
        """ Install bbtest package on remote host.

        :param bbtest_version: bbtest version to install.
        """
        super().install()
        root_dir = os.path.dirname(os.path.dirname(os.path.join(os.path.dirname(__file__), 'src')))
        dist_dir = os.path.join(root_dir, 'dist')
        if not bbtest_version:
            def _extract_version(f):
                return float(f.split('-')[-1].split('.tar.gz')[0])
            bbtest_packages = glob.glob(os.path.join(dist_dir, 'bbtest-*.tar.gz'))
            try:
                bbtest_package = max(bbtest_packages, key=_extract_version)
            except Exception as e:
                raise Exception(f'Failed to find bbtest package - {e}')
        bbtest_remote = self.put(bbtest_package, bbtest_package.replace('\\', '/').split('/')[-1])
        args = ['py', '-3'] if 'win' in self.modules.platform.platform().lower() else ['python3']
        args.extend(['-m', 'pip', 'install', '-U', bbtest_remote])
        self.modules.subprocess.run(args, stdout=subprocess.PIPE)

    def put(self, local, remote):
        """ Put file on target host relative to root path. """
        relative_remote = self._relative_remote(remote)
        self.ftp.storbinary(f'STOR {relative_remote}', open(local, 'rb'))
        return os.path.join(self.root_path, relative_remote).replace('\\', '/')

    def get(self, remote, local):
        """ Get file from target host relative to root path. """
        relative_remote = self._relative_remote(remote)
        self.ftp.retrbinary(f'RETR {relative_remote}', open(local, 'wb').write)
        return local

    def run(self, args, **kwargs):
        rpyc_kwargs = {k: v for k, v in kwargs.items() if k in self._rpyc._config}
        for key, value in rpyc_kwargs.items():
            self._rpyc._config[key] = value
        self._rpyc._config['sync_request_timeout'] = kwargs.pop('timeout', self._rpyc._config['sync_request_timeout'])
        try:
            output = super().run(args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self._rpyc._config['sync_request_timeout'] = SYNC_REQUEST_TIMEOUT
        return output

    def mkdtemp(self, **kwargs):
        """ same args as tempfile.mkdtemp """
        if 'dir' not in kwargs:
            kwargs['dir'] = self.root_path
        return self.modules.bbtest.LocalHost.mkdtemp(**kwargs)

    def rmtree(self, *args, **kwargs):
        return self.modules.bbtest.LocalHost.rmtree(*args, **kwargs)

    def rmfile(self, path):
        return self.modules.bbtest.LocalHost.rmfile(path)

    def rmfiles(self, name):
        return self.modules.bbtest.LocalHost.rmfiles(name)

    def is_process_running(self, process, timeout=1):
        return self.modules.bbtest.LocalHost.is_process_running(process, timeout)

    def isfile(self, path):
        return self.modules.bbtest.LocalHost().isfile(path)

    def untar_file(self, path):
        return self.modules.bbtest.LocalHost().untar_file(path)

    def _relative_remote(self, remote):
        return remote.replace('\\', '/').replace(self.root_path, '').lstrip('/')


class WindowsHost(RemoteHost):
    """ A remote windows host """
    ROOT_PATH = 'c:/temp'

    def __init__(self, ip="localhost", auth=("user", "pass")):
        super().__init__(ip, auth)

    def get_package_version(self, package_name):
        return self.modules.bbtest.LocalWindowsHost().get_package_version(package_name)

    def open_key(self, parent_key, key):
        return self.modules.bbtest.LocalHost.open_key(parent_key, key)

    def get_active_macs(self):
        return self.modules.bbtest.LocalWindowsHost().get_active_macs()

    def is_service_running(self, service):
        return self.modules.bbtest.LocalWindowsHost.is_service_running(service)


class LinuxHost(RemoteHost):

    ROOT_PATH = '/tmp'

    def is_service_running(self, service):
        return self.modules.bbtest.LocalLinuxHost.is_service_running(service)


class FedoraHost(LinuxHost):
    pass


class DebianHost(LinuxHost):
    pass


class OSXHost(RemoteHost):

    ROOT_PATH = '/tmp'

    def is_service_running(self, service):
        return self.modules.bbtest.LocalOSXHost().is_service_running(service)
