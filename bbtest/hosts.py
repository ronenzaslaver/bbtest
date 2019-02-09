"""
Hosts in the network.
"""
import logging
import os
import stat
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
import re
try:
    from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumKey, QueryValueEx
except Exception:
    pass

from .exceptions import ImproperlyConfigured

SYNC_REQUEST_TIMEOUT = 120
DEFAULT_RPYC_SERVER_PORT = os.environ.get('BBTEST_DEFAULT_RPYC_SERVER_PORT', 57911)
INSTALL_RECONNECT_WAIT = os.environ.get('BBTEST_INSTALL_RECONNECT_WAIT', 1)
platform_shotname_re = re.compile('.*(windows|debian|centos).*')

logger = logging.getLogger('bblog')


def getmodule(name):
    """imports an arbitrary module"""
    try:
        module = __import__(name, None, None, "*")
    except Exception as _:
        module = __import__(f'bbtest.{name}', None, None, "*")
    return module


class BaseHost(object):
    """"A base host class

    :param SEP: The path separator character
    :type SEP: str
    """

    SEP = '/'

    def __init__(self, *args, **kwargs):
        self.args = args
        self.params = kwargs
        self.root_path = getattr(self, 'ROOT_PATH', tempfile.gettempdir())

    def install(self, *args, **kwargs):
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
    def is_winodws(self):
        return 'windows' in self.os

    @property
    def is_linux(self):
        return 'linux' in self.os

    @property
    def os(self):
        """ Returns a lower case string identifying the OS. """
        return self.modules.platform.system().lower()

    @property
    def os_bits(self):
        """ Returns the OS bits architecture - 32 or 64. """
        return int(self.modules.platform.machine()[-2:])

    @property
    def platform(self):
        """ Returns the platform short, beautify, name - windows/debian/fedora. """
        return platform_shotname_re.findall(self.modules.platform.platform().lower())[0]

    @property
    def hostname(self):
        return self.modules.socket.gethostname()

    @property
    def name(self):
        return self.params.get('name', self.hostname)

    @property
    def is_local(self):
        return isinstance(self, LocalHost)

    @property
    def is_remote(self):
        return isinstance(self, RemoteHost)

    def rmfiles(self, top):
        try:
            for root, dirs, files in self.modules.os.walk(top):
                for file in files:
                    self.modules.os.remove(os.path.join(root, file))
                for dir in dirs:
                    self.modules.shutil.rmtree(os.path.join(root, dir))
        except OSError:
            pass

    def mkdtemp(self, **kwargs):
        """ same args as tempfile.mkdtemp """
        if 'dir' not in kwargs:
            kwargs['dir'] = self.root_path
        return self.modules.tempfile.mkdtemp(**kwargs)

    def chmod_777(self, path):
        # on my ubuntu 18.0.4 chmod with 0x777 didn't set write permission for owner?
        self.modules.os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    def run(self, args, **kwargs):
        logger.debug(f'{self.__class__.__name__} run command: {args} {kwargs}')
        shutils_kwargs = {k: v for k, v in kwargs.items() if k not in rpyc.core.protocol.DEFAULT_CONFIG}
        output = self.modules.target.subprocess_run(args, **shutils_kwargs)
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

    def download_file(self, src_url, dst_path):
        dst = self.modules.target.download_file(src_url, dst_path)
        self.chmod_777(dst)
        return dst


class LocalHost(BaseHost):
    """Suppose to be an os-agnostic local host."""
    ip = '127.0.0.1'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules = rpyc.core.service.ModuleNamespace(getmodule)

    def put(self, local, remote):
        """ Put file on target host relative to root path. """
        dst = shutil.copyfile(local, self._relative_remote(remote))
        self.chmod_777(dst)
        return dst

    def get(self, remote, local):
        """ Get file from target host relative to root path. """
        return shutil.copyfile(self._relative_remote(remote), local)

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
        return os.path.join(self.root_path, remote.replace('\\', '/').replace(self.root_path, '').lstrip('/'))


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

    def __init__(self, ip=None, auth=None, *args, **kwargs):
        """ Initialise remote host - open FTP and rpyc connections.

        :param ip:
        :param auth:
        """
        super().__init__(*args, **kwargs)
        self.ip = str(ip)
        self.auth = auth
        self.ftp = FTP(self.ip)
        try:
            if auth:
                self.ftp.login(self.auth['user'], self.auth['password'])
            else:
                # Assume anonymous
                self.ftp.login()
        except Exception as e:
            raise ConnectionError(f'Failed to connect to FTP server on host {self.ip} - {e}')
        rpyc.core.protocol.DEFAULT_CONFIG['sync_request_timeout'] = SYNC_REQUEST_TIMEOUT
        self._start_rpyc()

    def install(self, package=None, version=None):
        """ Install bbtes=Nonet tests package on remote host.

        :param package: bbtest tests package to install. If None do not install
        :param version: package version to install, if None install latest
        """

        super().install()
        if not package:
            return

        pip_index = self.params.get('pip_index', None)
        if not pip_index:
            raise ImproperlyConfigured(f'need to install package {package} but no pypi')
        if pip_index.startswith('http'):
            bbtest_remote = f'-i {pip_index} {package}'.split()
        else:
            if not version:
                def _extract_version(f):
                    return f.split('-')[-1].split('.tar.gz')[0]
                bbtest_packages = glob.glob(os.path.join(pip_index, package + '-*'))
                try:
                    bbtest_package = max(bbtest_packages, key=_extract_version)
                except Exception as e:
                    raise Exception(f'Failed to find bbtest package - {e}')
            else:
                bbtest_package = os.path.join(pip_index, package + '-' + version)
            bbtest_remote = [self.put(bbtest_package, bbtest_package.replace('\\', '/').split('/')[-1])]
        # it is problematic to rely on bbtest operations to install bbtest because if they change it requires manual\
        # update of bbtest on remote host.
        # todo: consider replace all code below with atomic commands directly over self.modeules
        rc = self.run_python3(['-m', 'pip', 'install', '-U'] + bbtest_remote)
        if self.is_linux:
            try:
                self.run(['systemctl', 'restart', 'rpycserver.service'])
            except Exception as _:
                pass
            time.sleep(INSTALL_RECONNECT_WAIT)
            self._start_rpyc()

    def put(self, local, remote):
        """ Put file on target host relative to root path. """
        relative_remote = self._relative_remote(remote)
        self.ftp.storbinary(f'STOR {relative_remote}', open(local, 'rb'))
        dst = os.path.join(self.root_path, relative_remote).replace('\\', '/')
        self.chmod_777(dst)
        return dst

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

    def untar_file(self, path):
        return self.modules.bbtest.LocalHost().untar_file(path)

    def _start_rpyc(self):
        try:
            self._rpyc = rpyc.classic.connect(self.ip, port=DEFAULT_RPYC_SERVER_PORT)
        except Exception as e:
            raise ConnectionError(f'Failed to connect to RPyC server on host {self.ip} - {e}')
        self.modules = self._rpyc.modules

    def _relative_remote(self, remote):
        return remote.replace('\\', '/').replace(self.root_path, '').lstrip('/')


class WindowsHost(RemoteHost):
    """ A remote windows host """
    ROOT_PATH = 'c:/temp'

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


class OSXHost(RemoteHost):

    ROOT_PATH = '/tmp'

    def is_service_running(self, service):
        return self.modules.bbtest.LocalOSXHost().is_service_running(service)
