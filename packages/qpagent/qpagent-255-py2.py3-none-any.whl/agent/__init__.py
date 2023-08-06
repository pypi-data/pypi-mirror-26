#!/usr/bin/env python
# -*- coding: utf-8 -*-
from logging.config import dictConfig
from subprocess import Popen, PIPE

describe = 'git rev-list --count HEAD'
version = Popen(describe.split(), stdout=PIPE).communicate()[0].strip()
__version__ = 255

LOGGING_CONFIG = dict({
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'shortener': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'formatters': {
        'console': {
            'format': '%(asctime)s [%(levelname)s] [%(name)s][%(process)d]'
                      ': %(message)s',
        },
    }
})
dictConfig(LOGGING_CONFIG)
