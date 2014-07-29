import abc
import re
from yapsy.IPlugin import IPlugin

INPUT_PATTERN_REGISTRY = {}

class UserInput(IPlugin):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def register_plugin(self, pattern_registry):
		return false

def handle_input(msg):
    for pattern in INPUT_PATTERN_REGISTRY.iterkeys():
        if re.match(pattern, msg):
            INPUT_PATTERN_REGISTRY[pattern](msg)
