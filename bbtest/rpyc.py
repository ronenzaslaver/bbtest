
import rpyc

from bbtest.hosts import getmodule


class BBTestSlave(rpyc.core.service.Slave):
    def getmodule(self, name):
        """imports an arbitrary module"""
        return getmodule(name)


class BBTestService(BBTestSlave, rpyc.Service):
    """The SlaveService allows the other side to perform arbitrary imports and
    execution arbitrary code on the server. This is provided for compatibility
    with the classic RPyC (2.6) modus operandi.

    This service is very useful in local, secure networks, but it exposes
    a **major security risk** otherwise."""
    __slots__ = ()

    def on_connect(self, conn):
        self._conn = conn
        self._conn._config.update(dict(
            allow_all_attrs=True,
            allow_pickle=True,
            allow_getattr=True,
            allow_setattr=True,
            allow_delattr=True,
            allow_exposed_attrs=False,
            import_custom_exceptions=True,
            instantiate_custom_exceptions=True,
            instantiate_oldstyle_exceptions=True,
        ))
        super(BBTestService, self).on_connect(conn)
