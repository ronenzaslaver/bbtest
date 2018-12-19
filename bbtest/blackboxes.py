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

    def remove(self):
        """Removing the black box from `self.host`"""
        pass
