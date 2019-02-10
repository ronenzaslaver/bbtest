#!/usr/bin/env python

import os
from plumbum import cli
import rpyc
from rpyc.lib import setup_logger
from rpyc.utils.server import ThreadedServer
from rpyc.utils.classic import DEFAULT_SERVER_PORT, DEFAULT_SERVER_SSL_PORT
from rpyc.utils.authenticators import SSLAuthenticator


DEFAULT_RPYC_SERVER_PORT = os.environ.get('BBTEST_DEFAULT_RPYC_SERVER_PORT', 57911)
DEFAULT_RPYC_SERVER_SSL_PORT = os.environ.get('BBTEST_DEFAULT_RPYC_SERVER_SSL_PORT', 57911)


class BbtestSlave(rpyc.core.service.Slave):
    def getmodule(self, name):
        """imports an arbitrary module"""
        try:
            module = __import__(name, None, None, "*")
        except Exception as _:
            module = __import__(f'bbtest.{name}', None, None, "*")
        return module


class BbtestService(BbtestSlave, rpyc.Service):
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
        super(BbtestService, self).on_connect(conn)


class BbtestServer(cli.Application):

    host = cli.SwitchAttr(["--host"], str, default="127.0.0.1", group="Socket Options",
                          help="The host to bind to. Default is localhost")
    port_help = (f"The TCP listener port (default = {DEFAULT_RPYC_SERVER_PORT},"
                 "default for SSL = {DEFAULT_RPYC_SERVER_SSL_PORT}")
    port = cli.SwitchAttr(["-p", "--port"], cli.Range(0, 65535), default=DEFAULT_RPYC_SERVER_PORT,
                          group="Socket Options", help=port_help)

    logfile = cli.SwitchAttr("--logfile", str, default=None, group="Logging",
                             help="Specify the log file to use; the default is stderr")
    quiet = cli.Flag(["-q", "--quiet"], group="Logging",
                     help="Quiet mode (only errors will be logged)")

    ssl_keyfile = cli.SwitchAttr("--ssl-keyfile", cli.ExistingFile, group="SSL", requires=["--ssl-certfile"],
                                 help="The keyfile to use for SSL. Required for SSL")
    ssl_certfile = cli.SwitchAttr("--ssl-certfile", cli.ExistingFile, group="SSL", requires=["--ssl-keyfile"],
                                  help="The certificate file to use for SSL. Required for SSL")
    ssl_help = "The certificate authority chain file to use for SSL. Optional; enables client-side authentication"
    ssl_cafile = cli.SwitchAttr("--ssl-cafile", cli.ExistingFile, group="SSL", requires=["--ssl-keyfile"],
                                help=ssl_help)

    def main(self):
        if self.ssl_keyfile:
            self.authenticator = SSLAuthenticator(self.ssl_keyfile, self.ssl_certfile, self.ssl_cafile)
            default_port = DEFAULT_SERVER_SSL_PORT
        else:
            self.authenticator = None
            default_port = DEFAULT_SERVER_PORT
        if self.port is None:
            self.port = default_port

        setup_logger(self.quiet, self.logfile)

        server = ThreadedServer(BbtestService, hostname=self.host, port=self.port, authenticator=self.authenticator)
        server.start()


def main():
    BbtestServer()


if __name__ == "__main__":
    main()
