import sys
import yaml

import logging
import logging.config

from twisted.internet import reactor, ssl
from irc import ListenerFactory
from yapsy.PluginManager import PluginManager

from plugins import UserInput, INPUT_PATTERN_REGISTRY

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
            'level': 'DEBUG',
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

# Prepare the plugin system
manager = PluginManager()
manager.setPluginPlaces(["plugins"])
manager.setCategoriesFilter({
    "Input": UserInput,
})

manager.collectPlugins()

for plugin in manager.getPluginsOfCategory("Input"):
    plugin.plugin_object.register_plugin(pattern_registry)

# Prepare the global settings object.
with open('settings.yaml', 'r') as f:
    GLOBAL_SETTINGS = yaml.load(f)

# Main function
if __name__ == '__main__':
    f = ListenerFactory(GLOBAL_SETTINGS["server"])

    reactor.connectSSL(GLOBAL_SETTINGS["server"]["host"], GLOBAL_SETTINGS["server"]["port"], f, ssl.ClientContextFactory())
    
    reactor.run()
