"""
Hosts in the network.
"""
import subprocess
import sys
from shutil import copyfile


class Host(object):

    def __init__(self, ip=None, username=None, password=None):
        self.ip = ip
        self.username = username
        self.password = password

    def install(self, downloads_dir, **kwargs):
        pass

    def clean(self):
        pass


class LocalHost(Host):

    @property
    def os(self):
        return sys.platform

    @property
    def temp_dir(self):
        if self.os == 'win32':
            return 'c:/temp'
        elif self.os == 'linux':
            return '/tmp'
        else:
            return None

    def run(self, cmd, *args):
        args_list = list(args) if args else []
        output = subprocess.run([cmd] + args_list, stdout=subprocess.PIPE)
        return output.stdout.decode('utf-8').strip().split('\n')

    def put(self, local, remote):
        return copyfile(local, remote)


class WindowsHost(Host):

    @property
    def os(self):
        return 'win32'


class LinuxHost(Host):

    @property
    def os(self):
        return 'linux'


class MacHost(Host):
    pass
