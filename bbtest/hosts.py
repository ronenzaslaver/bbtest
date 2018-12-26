"""
Hosts in the network.
"""
import os
import subprocess
import sys
import shutil
import tempfile


class BaseHost(object):

    SEP = '/'
    BIT = None
    OS = None
    PACKAGE_TYPE = None

    def __init__(self, ip=None, username=None, password=None):
        self.ip = ip
        self.username = username
        self.password = password

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


class LocalHost(BaseHost):

    def __init__(self):
        super().__init__('localhost')

    @property
    def os(self):
        return sys.platform

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


class WindowsHost(BaseHost):

    OS = 'win'
    BIT = None
    PACKAGE_TYPE = 'msi'

    def __init__(self, image='Window7 SP2'):
        """Deploy a host and store its address and credentials"""
        pass

    def destroy(self):
        """Release the host"""
        pass


class Windows32Host(WindowsHost):

    BIT = '32'


class Windows64Host(WindowsHost):

    BIT = '64'


class LinuxHost(BaseHost):

    OS = 'linux'


class CentOSHost(LinuxHost):

    PACKAGE_TYPE = 'rpm'


class DebianHost(LinuxHost):

    PACKAGE_TYPE = 'deb'


class OSXHost(BaseHost):

    OS = 'osx'
    PACKAGE_TYPE = 'pkg'
