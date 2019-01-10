"""
To take part in a test a component needs to be wrapped in a BlackBox.
"""
import logging
from os import path

logger = logging.getLogger('bblog')


class BlackBox():
    """This is an abstract class used to wrap a component in a black box.
    Black boxes can then be used to test the component itself and to verify
    it integrates well with other components.
    A blackbox runs on a host and you can communicate with it using `host.run`
    """

    def __init__(self, host, name=None):
        self.host = host
        self.name = name if name else self.__class__.__name__[:-3].lower()

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
        return self.host.mkdtemp(prefix=f"blackbox_{self.NAME}_")


class HomeBox(BlackBox):
    """A black box with a home folder"""

    NAME = 'home'

    def install(self):
        """Create a temp dir and store it in `self.path`"""
        super().install()
        self.path = self.mkdtemp()
        logger.debug(f"HomeBox.install made a home in {self.path}")

    def uninstall(self):
        """Remove the home path"""
        self.host.rmtree(self.path)
        super().uninstall()

    def clean(self):
        """Remove all files from home"""
        if self.host and self.path:
            self.host.rmfiles(self.path)

    def run(self, *args, **kwargs):
        return self.host.run(*args, cwd=self.path, **kwargs)

    def put(self, src, dest, *args, **kwargs):
        """Put a file in the host's home directory """
        return self.host.put(
            src, self.host.join(self.path, dest), *args, **kwargs)

    def run_file(self, src_path, background=False, params=None):
        """Copy the source to the box, run it, and return its output."""
        basename = path.basename(src_path)
        self.put(src_path, basename)

        if self.host.os.startswith('linux'):
            self.run(f'chmod 777 {basename}')
        self.run(f'./{basename} ' + ' '.join(params))