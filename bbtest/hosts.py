"""
Hosts in the network.
"""
import os
import platform
import subprocess
import shutil
import tempfile
from winreg import HKEY_LOCAL_MACHINE, OpenKey, EnumKey, QueryValueEx

import psutil
from psutil import NoSuchProcess


class BaseHost(object):
    """"A base host class

    :param SEP: The path separator character
    :type SEP: str

    """
    SEP = '/'

    def __init__(self, ip=None, username=None, password=None):
        self.ip = ip
        self.username = username
        self.password = password

    @property
    def os(self):
        return platform.platform()

    @property
    def bit(self):
        return platform.architecture()[0][0:2]

    @property
    def package_type(self):
        if 'windows' in self.os.lower():
            return 'msi'
        else:
            raise NotImplementedError('Non Windows OS')

    def destroy(self):
        """Release the host"""
        pass

    def uninstall(self):
        """ the opposite of install,  uninstall our tools from the host """
        pass

    def clean(self):
        pass

    def join(self, *args):
        return self.SEP.join(args)

    def mkdtemp(self, **kwargs):
        """ same args as tempfile.mkdtemp """
        pass

    def rm(self, path, recursive=False, force=False):
        pass

    def isfile(self, path):
        pass

    # TODO: remove the next methods as they are too specific
    def rmtree(self, path, ignore_errors=True, onerror=None):
        pass

    def rmfile(self, path):
        pass

    def run_python2(self, *args, **kwargs):
        """Call run command with python2 as the process"""
        pass


class LocalHost(BaseHost):

    def __init__(self):
        super().__init__('localhost')

    @property
    def os(self):
        return platform.platform()

    @property
    def bit(self):
        return platform.architecture()[0][0:2]

    @property
    def package_type(self):
        if 'windows' in self.os.lower():
            return 'msi'
        else:
            raise NotImplementedError('Non Windows OS')

    def run(self, cmd, *args, **kwargs):
        args_list = list(args) if args else []
        output = subprocess.run(
            [cmd] + args_list, stdout=subprocess.PIPE, **kwargs)
        return output.stdout.decode('utf-8').strip().split('\n') if output.stdout else []

    def put(self, local, remote):
        return shutil.copyfile(local, remote)

    def mkdtemp(self, **kwargs):
        return tempfile.mkdtemp(**kwargs)

    def rm(self, path, recursive=False, force=False):
        options = list()
        if recursive:
            options.append('-r')
        if force:
            options.append('-f')
        options.append(path)
        return self.run('rm', *options)

    def rmtree(self, path, ignore_errors=True, onerror=None):
        return shutil.rmtree(path, ignore_errors, onerror)

    def rmfile(self, path):
        try:
            os.remove(path)
        except OSError:
            pass

    def rmfiles(self, path):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    os.remove(os.path.join(root, file))
                for dir in dirs:
                    self.rmtree(os.path.join(root, dir))
        except OSError:
            pass

    def isfile(self, path):
        return os.path.isfile(path)

    def run_python2(self, *args, **kwargs):
        if 'win' in self.os.lower():
            python_executable = ['py', '-2']
        else:
            python_executable = ['python2']
        return self.run(*python_executable, *args, **kwargs)

    @staticmethod
    def is_process_running(process_name):
        for process in psutil.process_iter():
            if process.name() == process_name:
                return True
        return False

    def is_service_running(self, service_name):
        if 'win' in self.os.lower():
            try:
                return psutil.win_service_get(service_name).status() == 'running'
            except NoSuchProcess:
                return False
        else:
            raise NotImplementedError('Non Windows os')

    @staticmethod
    def is_package_installed(package_name):
        key_val = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall'
        products = OpenKey(HKEY_LOCAL_MACHINE, key_val)
        try:
            i = 0
            while True:
                product_key_name = EnumKey(products, i)
                product_values = OpenKey(products, product_key_name)
                try:
                    product_display_name = QueryValueEx(product_values, 'DisplayName')[0]
                    if product_display_name == package_name:
                        return True
                except FileNotFoundError:  # product has no 'DisplayName' attribute
                    pass
                i = i+1
        except WindowsError:
            return False


class WindowsHost(BaseHost):

    def __init__(self, image='Window7 SP2'):
        """Deploy a host and store its address and credentials"""
        pass

    def destroy(self):
        """Release the host"""
        pass


class LinuxHost(BaseHost):
    pass


class OSXHost(BaseHost):
    pass
