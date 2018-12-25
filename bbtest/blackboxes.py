"""
To take part in a test a component needs to be wrapped in a BlackBox.
"""
from os import path


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

    def mkdtemp(self, **kwagrs):
        """Create a temp directory"""
        return self.host.mkdtemp(prefix=f"blackbox_{self.NAME}_")

    def uninstall(self):
        """Removing the black box from `self.host`"""
        pass

    def clean(self):
        pass


class HomeBox(BlackBox):
    """A black box with a home folder"""

    NAME = 'home'

    def run(self, *args, **kwargs):
        return self.host.run(*args, cwd=self.path, **kwargs)

    def install(self):
        """Create a temp dir and store it in `self.path`"""
        self.path = self.mkdtemp()

    def clean(self):
        """Remove all files from home"""
        if self.host and self.path:
            self.host.rm(self.path+'/*', recursive=True)

    def put(self, src, dest, *args, **kwargs):
        """Put a file in thost's home directory """
        return self.host.put(
            src, self.host.join(self.path, dest), *args, **kwargs)

    def remove(self):
        """Remove the home path"""
        return self.host.rmtree(self.path)

    def run_file(self, src_path, background=False, params=None):
        """Copy the source to the box, run it, and return its output."""
        basename = path.basename(src_path)
        self.put(src_path, basename)

        self.run('chmod', '777', basename)
        self.run(f'./{basename}', *params)


class SpyServerBox(BlackBox):
    """A box that exposes a `url` and a `log` so that any messages POSTed to
    url is appended to the log.

    .. important:: It still doesn't work and the log never changes
    """

    NAME = 'serverspy'

    log = ['Hello Sara!']
    """log is an array of log messages where Each POSTed message is appended"""

    def install(self):
        self.url = "http://example.com"

    def clean(self):
        pass
