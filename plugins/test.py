import plugins

class TestInputPlugin(plugins.UserInput):
    def register_plugin(self, pattern_registry):
        pattern_registry['.+'] = self.test_input

    def test_input(self, msg):
        print "Plugin input: " + msg
