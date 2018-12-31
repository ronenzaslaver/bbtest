
"""
General services and utilities to communicate with the development ecosystem.

Logger
File server
...
"""

import logging.config

from .logging_dicts import crlogs_dict


logging.config.dictConfig(crlogs_dict)
logger = logging.getLogger()


class FileServer(object):
    """ File server service. """

    def __init__(self, host, root_dir):
        """
        :param host: file server host.
        :param type: BaseHost
        :param root_dir: full path to root directory on the host.
        :param root_dir: BaseHost
        """
        self.host = host
        self.root_dir = root_dir

    def put(self, source, destination=None):
        """ Put source file on the file server in destination location.

        :todo implement str and StringIO.
        :param source: source file path or file descriptor.
        :type source: str, File or StringIO.
        :param destination: destination file path on the file server relative to the file server root directory,
            If None determine destination.
        :return: destination file path on the file server relative to the file server root directory.
        """
        pass

    def get(self, source, destination=None):
        """ Get source file from file server and (optionally) place it on destination location.

        :param source: path to source file on the file server (relative to root directory)
        :param destination: full path to destination file, if None a file StringBuffer will be returned.
        :return:
        """
        pass
