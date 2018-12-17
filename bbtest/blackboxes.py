"""
Base black boxes.
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

    def start(self):
        pass


class lab(BlackBox):
    pass


class HostBox(BlackBox):
    pass


class EndpointBox(BlackBox):

    def install(self, what):
        return self.host.install(what)
