"""
To take part in a test a component needs to be wrapped in a BlackBox.
"""

import logging

logger = logging.getLogger('bblog')


class BlackBox():
    """This is an abstract class used to wrap a component in a black box.
    Black boxes can then be used to test the component itself and to verify
    it integrates well with other components.
    A blackbox runs on a host and you can communicate with it using `host.run`
    """

    def __init__(self, name, host, **kwargs):
        self.name = name
        self.host = host
        self.params = kwargs

    def __repr__(self):
        return self.name

    def install(self):
        """Installing the black box on `self.host`"""
        pass

    def uninstall(self):
        """Removing the black box from `self.host`"""
        pass

    def clean(self):
        pass

    def mkdtemp(self, **kwagrs):
        """Create a temp directory"""
        temp = self.host.mkdtemp(prefix=f"blackbox_{self.name}_")
        self.host.chmod_777(temp)
        return temp


class HomeBox(BlackBox):
    """A black box with a home folder"""

    def __init__(self, name, host, **kwargs):
        super().__init__(name, host, **kwargs)
        self.path = None

    def install(self):
        """Create a temp dir and store it in `self.path`"""
        super().install()
        self.path = self.mkdtemp()
        logger.debug(f"HomeBox.install made a home in {self.path}")

    def uninstall(self):
        """Remove the home path"""
        try:
            if self.path:
                self.host.modules.shutil.rmtree(self.path)
        except OSError:
            pass
        super().uninstall()

    def clean(self):
        """Remove all files from home"""
        if self.host and self.path:
            self.host.rmfiles(self.path)

    def run(self, args, **kwargs):
        return self.host.run(args, cwd=self.path, **kwargs)

    def put(self, local, remote):
        """Put a file in the box's home directory """
        return self.host.put(local, self.host.join(self.path, remote))

    def get(self, remote, local):
        """ Get file from the box's home directory. """
        return self.host.get(self.host.join(self.path, remote), local)

    def isfile(self, path):
        return self.host.modules.os.path.isfile(self.host.join(self.path, path))

    def rmfile(self, path):
        return self.host.modules.os.remove(self.host.join(self.path, path))
