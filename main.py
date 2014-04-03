import sys

import logging
import logging.config

from twisted.internet import reactor, ssl
from irc import ListenerFactory

# Configure logging.
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)-8s] %(asctime)s -- %(message)s',
        },
        'brief': {
            'format': '[%(levelname)-8s] -- %(message)s',
        },
    },

    'handlers': {
        'file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'adventurebot.log',
            'formatter': 'verbose',
            'maxBytes': 262144,
            'backupCount': 1,
        },
        'console_handler': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'brief',
        },
    },

    'loggers': {
        'irc': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'game': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'WARN',
            'propagate': False,
        },
        'interpreter': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'WARN',
            'propagate': False,
        },
        'commands': {
            'handlers': ['file_handler', 'console_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

# Main function
if __name__ == '__main__':
    f = ListenerFactory()
    reactor.connectSSL("irc.cat.pdx.edu", 6697, f, ssl.ClientContextFactory())
    reactor.run()
