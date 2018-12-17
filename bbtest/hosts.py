"""
Hosts in the network.
"""


class Host(object):
    def install(self, downloads_dir, **kwargs):
        pass


class WindowsHost(Host):
    pass


class LinuxHost(Host):
    pass


class MacHost(Host):
    pass
