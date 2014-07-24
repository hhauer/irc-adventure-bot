import abc
from yapsy.IPlugin import IPlugin

INPUT_PATTERN_REGISTRY = {}

class UserInput(IPlugin):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def register_plugin(self, pattern_registry):
		return false