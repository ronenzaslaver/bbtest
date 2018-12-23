"""
To take part in a test a component needs to be wrapped in a BlackBox.
"""


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


class HomeBox(BlackBox):
    """A black box with a home folder """

    NAME = 'home'

    def run(self, *args, **kwargs):
        self.host.run(*args, cwd=self.path, **kwargs)

    def install(self):
        self.path = self.mkdtemp()

    def clean(self):
        if self.host and self.path:
            self.host.rm(self.path+'/*', recursive=True)

    def remove(self):
        """Clean's job is to wipe all data. In todo's case, it's just a file"""
        return self.host.rmtree(self.path)


class ServerSpyBox(BlackBox):

    NAME = 'serverspy'

    # TODO: we need to be smarter than this and log the POSTed data
    log = ['Hello Sara!']

    def install(self):
        self.url = "http://example.com"

    def clean(self):
        pass

