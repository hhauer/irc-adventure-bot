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
    # Twisted IRC Values
    nickname = 'AdventureBot'
    realname = 'Adventure'
    username = 'Adventure'
    linerate = 1

    # AdventureBot Values
    output_channel = '#adventurebot'
    input_channels = ['#informationsociety']
    engine = Engine()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

        # Join listen channels.
        for x in self.input_channels:
            self.join(x)

        # join output channel.
        self.join(self.output_channel)

        self.users = {}

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]

        if user not in self.users:
            self.users[user] = User(user)

        if channel in self.input_channels:
            energy = self.engine.process_message(self.users[user], Message(message))
            self.msg(self.output_channel, "{} -- [{}] Line: {} | Total: {}".format(channel, user, energy, self.users[user].energy))
        elif channel == self.nickname:
            self.msg(self.output_channel, "Received private message from {}".format(user))
        else:
            self.msg(self.output_channel, "Input from invalid source.")


class ListenerFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Listener()

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()
