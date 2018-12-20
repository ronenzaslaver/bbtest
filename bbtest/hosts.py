"""
Hosts in the network.
"""
import os
import subprocess
import sys
import shutil
import tempfile


class BaseHost(object):
    _SEP = '/'

    def __init__(self, ip=None, username=None, password=None):
        self.ip = ip
        self.username = username
        self.password = password

    def install(self, downloads_dir, **kwargs):
        pass

    def remove(self):
        """ the opposite of install, completly remove the host """
        pass

    def clean(self):
        pass

    def join(self, *args):
        return self._SEP.join(args)

    def mkdtemp(self, **kwargs):
        """ same args as tempfile.mkdtemp """
        pass

    def rmtree(self, path, ignore_errors=True, onerror=None):
        pass

    def rmfile(self, path):
        pass


class LocalHost(BaseHost):

    @property
    def os(self):
        return sys.platform

    def run(self, cmd, *args):
        args_list = list(args) if args else []
        output = subprocess.run([cmd] + args_list, stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8').strip().split('\n')

    def put(self, local, remote):
        return shutil.copyfile(local, remote)

    def mkdtemp(self, **kwargs):
        return tempfile.mkdtemp(**kwargs)

    def rmtree(self, path, ignore_errors=True, onerror=None):
        return shutil.rmtree(path, ignore_errors, onerror)

    def rmfile(self, path):
        try:
            os.remove(path)
        except OSError:
            pass


class WindowsHost(BaseHost):

    @property
    def os(self):
        return 'win32'


class LinuxHost(BaseHost):

    @property
    def os(self):
        return 'linux'


class MacHost(BaseHost):
    pass
