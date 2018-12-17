"""
Hosts in the network.
"""
import os
from shutil import copyfile


class Host(object):
    def __init__(self, ip=None, username=None, password=None):
        self.ip = ip
        self.username = username
        self.password = password

    def install(self, downloads_dir, **kwargs):
        pass

class LocalHost(Host):

    def run(self, cmd):
        return os.system(cmd)

    def put(self, local, remote):
        return copyfile(local, remote)


class WindowsHost(Host):
    pass


class LinuxHost(Host):
    pass


class MacHost(Host):
    pass
