import logging
from logging.config import dictConfig

from informatics_diff.config import config

FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'


def configure_logging():
    dictConfig({
        'version': 1,
        'formatters': {
            'f': {
                'format': FORMAT,
            },
        },
        'handlers': {
            'h': {
                'class': 'logging.StreamHandler',
                'formatter': 'f',
                'level': config.logging_level,
            },
        },
        'root': {
            'handlers': ['h'],
            'level': logging.DEBUG,
        },
    })
