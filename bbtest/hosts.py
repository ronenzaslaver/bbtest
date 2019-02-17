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
import rpyc
import glob
import re

from .exceptions import ImproperlyConfigured

SYNC_REQUEST_TIMEOUT = 120
DEFAULT_RPYC_SERVER_PORT = int(os.environ.get('BBTEST_DEFAULT_RPYC_SERVER_PORT', 57911))
INSTALL_RECONNECT_WAIT = os.environ.get('BBTEST_INSTALL_RECONNECT_WAIT', 1)
platform_shotname_re = re.compile('.*(windows|debian|centos|ubuntu).*')

logger = logging.getLogger('bblog')


def getmodule(name):
    """imports an arbitrary module"""
    return __import__(name, None, None, "*")


class BaseHost(object):
    """"A base host class

    :param SEP: The path separator character
    :type SEP: str
    """

    SEP = '/'

    def __init__(self, name, **kwargs):
        self.name_ = name
        self.params = kwargs
        self.root_path = getattr(self, 'ROOT_PATH', tempfile.gettempdir())

    def __repr__(self):
        return self.name_

    def install(self, **kwargs):
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
    def is_windows(self):
        return self.modules.bbtest.osutils.is_windows()

    @property
    def is_linux(self):
        return self.modules.bbtest.osutils.is_linux()

    @property
    def is_mac(self):
        return self.modules.bbtest.osutils.is_mac()

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
        """ Returns the platform short, beautify, name - windows/debian/centos. """
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
        try:
            output = self.modules.bbtest.target.subprocess_run(args, **shutils_kwargs)
        except Exception as e:
            raise subprocess.SubprocessError(f'subprocess run "{args} {kwargs}" failed on target - {e}')
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
        args = ['py', '-' + str(version)] if self.is_windows else ['/opt/bbtest/python' + str(version)]
        args.extend(args_in)
        return self.run(args, **kwargs)

    def join(self, *args):
        return self.SEP.join(args)

    def download_file(self, src_url, dst_path):
        dst = self.modules.bbtest.target.download_file(src_url, dst_path)
        self.chmod_777(dst)
        return dst

    def _relative_remote(self, remote):
        return os.path.join(self.root_path, remote.replace('\\', '/').replace(self.root_path, '').lstrip('/')).replace('\\', '/')


class LocalHost(BaseHost):
    """Suppose to be an os-agnostic local host."""
    ip = '127.0.0.1'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
    def untar_file(path):
        if path.endswith('tar.gz'):
            tar = tarfile.open(path, "r:gz")
            tar.extractall(path=os.path.dirname(path))
            tar.close()
        else:
            # todo add the actual file extension to exception
            raise NotImplementedError('File extension is not supported')

    def set_client_timeout(self, timeout):
        # todo implement so users can set upper timeout (no need increase, just limit)
        pass


class LocalWindowsHost(LocalHost):

    """A collection of windows utilities and validators """
    ROOT_PATH = 'c:/temp'

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


class LocalOSXHost(LocalHost):

    ROOT_PATH = '/tmp'


class RemoteHost(BaseHost):
    """A remote host using RPyC
    """

    def __init__(self, ip=None, auth=None, **kwargs):
        """ Initialise remote host - open rpyc connections.

        :param ip:
        :param auth:
        """
        super().__init__(**kwargs)
        self.ip = str(ip)
        self.auth = auth
        rpyc.core.protocol.DEFAULT_CONFIG['sync_request_timeout'] = SYNC_REQUEST_TIMEOUT
        self._start_bbhost()

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
        # update of bbtest on remote host so we try to use atomic commands as possible.
        py3 = ['py', '-3'] if 'windows' in self.modules.platform.system().lower() else ['/opt/bbtest/python3']
        self.run(py3 + ['-m', 'pip', 'install', '-I', '-U', '--no-cache-dir'] + bbtest_remote)
        try:
            if self.is_linux:
                self.run(['systemctl', 'restart', 'bbhost.service'])
            elif self.is_windows:
                self.run(['bbhost_win_service.exe', 'restart'])
        except Exception as _:
            pass
        time.sleep(INSTALL_RECONNECT_WAIT)
        self._start_bbhost()

    def put(self, local, remote):
        """ Put file on target host relative to root path. """
        dst = self._relative_remote(remote)
        rpyc.utils.classic.upload_file(self._rpyc, local, dst)
        self.chmod_777(dst)
        return dst

    def get(self, remote, local):
        """ Get file from target host relative to root path. """
        relative_remote = self._relative_remote(remote)
        rpyc.utils.classic.download_file(self._rpyc, relative_remote, local)
        return local

    def run(self, args, **kwargs):
        rpyc_kwargs = {k: v for k, v in kwargs.items() if k in self._rpyc._config}
        for key, value in rpyc_kwargs.items():
            self._rpyc._config[key] = value
        self.set_client_timeout(kwargs.pop('timeout', self._rpyc._config['sync_request_timeout']))
        try:
            output = super().run(args, **kwargs)
        except Exception as e:
            raise e
        finally:
            self.set_client_timeout(SYNC_REQUEST_TIMEOUT)
        return output

    def untar_file(self, path):
        return self.modules.bbtest.LocalHost().untar_file(path)

    def set_client_timeout(self, timeout):
        self._rpyc._config['sync_request_timeout'] = timeout

    def _start_bbhost(self):
        port = self.params.get('port', DEFAULT_RPYC_SERVER_PORT)
        try:
            self._rpyc = rpyc.classic.connect(self.ip, port=port)
        except Exception as e:
            raise ConnectionError(f'Failed to connect to RPyC server on host {self.ip} port {port} - {e}')
        self.modules = self._rpyc.modules


class WindowsHost(RemoteHost):
    """ A remote windows host """
    ROOT_PATH = 'c:/temp'

    def get_active_macs(self):
        return self.modules.bbtest.LocalWindowsHost().get_active_macs()


class LinuxHost(RemoteHost):

    ROOT_PATH = '/tmp'


class OSXHost(RemoteHost):

    ROOT_PATH = '/tmp'
