
"""
"""

import logging.config

from .logging_dicts import crlogs_dict


logging.config.dictConfig(crlogs_dict)
logger = logging.getLogger()
