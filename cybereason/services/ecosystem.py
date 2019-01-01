
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
