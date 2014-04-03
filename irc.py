# Basic form largely from:
# http://twistedmatrix.com/documents/13.2.0/words/examples/ircLogBot.py

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.internet.error import ConnectionDone

import enchant
from enchant.tokenize import get_tokenizer

from game import Engine
from interpreter import Interpreter

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

    def __init__(self):
        self.users = {}

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        logger.info("Connection established.")

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        logger.info("Connection lost.")

    # Event callbacks.
    def signedOn(self):
       # Join listen channels.
        for x in self.input_channels:
            logger.debug("Joining listen channel %s.", x)
            self.join(x)

        # join output channel.
        logger.debug("Joining output channel %s.", self.output_channel)
        self.join(self.output_channel)

    def joined(self, channel):
        logger.info("Joined channel: %s.", channel)

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]

        if user not in self.users:
            self.users[user] = User(user)

        if channel in self.input_channels:
            energy = self.engine.process_message(self.users[user], Message(message))
            self.msg(self.output_channel, "{} -- [{}] Line: {} | Total: {}".format(channel, user, energy, self.users[user].energy))
        elif channel == self.nickname:
            i = Interpreter(self, self.engine, self.users[user], message)
            output = i.do_cmd()
            
            for l in output:
                self.msg(user, l)

    def action(self, user, channel, message):
        yield

    # IRC Callbacks
    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        #old_nick = prefix.split('!')[0]
        #new_nick = params[0]
        #self.logger.log("%s is now known as %s" % (old_nick, new_nick))


class ListenerFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Listener()

    def clientConnectionLost(self, connector, reason):
        r = reason.check(ConnectionDone)
        if r is ConnectionDone:
            print "Clean disconnect."
            reactor.stop()
        else:
            print "connection lost: ", reason
            connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()
