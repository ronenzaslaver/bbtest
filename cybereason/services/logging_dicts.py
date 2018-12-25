
from os import path, makedirs
import logging


log_dir = path.join(path.dirname(__file__), 'logs')
if not path.exists(log_dir):
    makedirs(log_dir)


crlogs_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.DEBUG,
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'filename': path.join(log_dir, 'cr_tests.log'),
            'formatter': 'standard',
            'maxBytes': 4194304,
            'mode': 'w+',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
            'propagate': True
        },
    }
}
