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

            output = (self.commands[self.tokens[0]](
                    self.listener,
                    self.engine,
                    self.user,
                    self.tokens[1:]
            ))

            if isinstance(output, list):
                for l in output:
                    self.output.append(l)
            else:
                self.output.append(output)
        
        except InvalidParametersException as e:
            self.output.append("The format of your command was not as expected.")
            self.output.append("Format: {}".format(e))
        except Exception as e:
            logger.warn("Exception in do_cmd: {}".format(e))
            self.output.append('That command was not recognized.')

        return self.output

    commands = {
            'set_password': do_set_password,
            'change_password': do_change_password,
            'authenticate': do_authenticate,
            'markov': do_markov,
    }

