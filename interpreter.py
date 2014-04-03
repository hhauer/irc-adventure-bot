from commands import *

# Logging
import logging
logger = logging.getLogger(__name__)

class Interpreter(object):
    def __init__(self, listener, engine, user, line):
        self.listener = listener
        self.engine = engine
        self.user = user
        self.tokens = line.split()

        # Output will be returned as an array after running a command.
        self.output = []
        logger.debug("Interpreter instantiated with line: {}".format(line))

    def do_cmd(self):
        try:
            logger.debug("Calling command {} with parameters {}.".format(
                self.tokens[0],
                self.tokens[1:]
            ))

            self.output = self.commands[self.tokens[0]](
                    self.listener,
                    self.engine,
                    self.user,
                    self.tokens[1:]
            )
        
        except Exception as e:
            logger.debug("Exception in do_cmd: {}".format(e))
            self.output = ['That command was not recognized.']

        return self.output

    commands = {
            'test': do_test,
    }

