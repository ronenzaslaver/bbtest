
"""
General services and utilities to communicate with the development ecosystem.

Logger
File server
...
"""

import os
import logging.config
import tempfile
import shutil

from .logging_dicts import crlogs_dict


logging.config.dictConfig(crlogs_dict)
logger = logging.getLogger()


class FileServer(object):
    """ File server service.

    Use to move files between remote hosts and to store files after test end and all temp/local files are gone.
    """

    def __init__(self, host, root_dir):
        """
        :param host: file server host.
        :type host: BaseHost
        :param root_dir: full path to root directory on the host.
        """
        self.host = host
        self.root_dir = tempfile.mkdtemp(prefix='bbtest_fileserver_', dir=root_dir)
        print(self.root_dir)

    def __del__(self):
        """ Clean temp file. """
        if os.path.isdir(self.root_dir):
            shutil.rmtree(self.root_dir)

    def put(self, source, destination):
        """ Put source file on the file server in destination location.

        :toto implement str and StringIO.
        :param source: source file path or file descriptor.
        :type source: str, File or StringIO.
        :param destination: destination file path on the file server relative to the file server root directory.
        :return: destination file path on the file server relative to the file server root directory.
        """
        return shutil.copy(source, self.root_dir + os.sep + destination)

    def get(self, source, destination=None):
        """ Get source file from file server and (optionally) place it on destination location.

        :param source: path to source file on the file server (relative to root directory)
        :param destination: full path to destination file. If empty return the content of the file.
        :return: requested file content.
        """
        if destination:
            shutil.copy(self.root_dir + os.sep + source, destination)
        else:
            with open(self.root_dir + os.sep + source, 'r') as f:
                content = f.read()
            return content
