from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

import enchant
from enchant.tokenize import get_tokenizer

from game import Engine

# Logging.
import logging
logger = logging.getLogger(__name__)

class User(object):
    def __init__(self, username):
        self.username = username
        self.energy = 0.00

class Message(object):
    tokenizer = get_tokenizer()
    dictionary = enchant.Dict()

    def __init__(self, line):
        self.tokens = [t[0] for t in self.tokenizer(line) if self.dictionary.check(t[0])]

class Listener(irc.IRCClient):
    nickname = 'AdventureBot'
    realname = 'AdventureBot'
    username = 'AdventureBot'
    linerate = 1

    engine = Engine()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.join('#informationsociety')
	self.join('#adventurebot')

        self.users = {}

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]

        if user not in self.users:
            self.users[user] = User(user)

        energy = self.engine.process_message(self.users[user], Message(message))
        self.msg('#adventurebot', "{} -- [{}] Line: {} | Total: {}".format(channel, user, energy, self.users[user].energy))

class ListenerFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Listener()

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()
