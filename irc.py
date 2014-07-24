# Basic form largely from:
# http://twistedmatrix.com/documents/13.2.0/words/examples/ircLogBot.py

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.internet.error import ConnectionDone

import enchant
from enchant.tokenize import get_tokenizer

from game import Engine
from interpreter import Interpreter
from models import User

# Logging.
import logging
logger = logging.getLogger(__name__)

class Message(object):
    tokenizer = get_tokenizer()
    dictionary = enchant.Dict()

    def __init__(self, line):
        self.tokens = [t[0] for t in self.tokenizer(line) if self.dictionary.check(t[0])]

class Listener(irc.IRCClient):
    # Twisted IRC Values
    #nickname = 'AdventureBot'
    #realname = 'Adventure'
    #username = 'Adventure'
    linerate = 1

    # AdventureBot Values
    output_channel = '#adventurebot'
    #input_channels = ['#informationsociety']
    engine = Engine()

    def __init__(self, options):
        self.users = {}
        self.nickname = options["nickname"]
        self.realname = options["realname"]
        self.username = options["username"]

        self.input_channels = options["channels"]

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
        self.msg(channel, "Now listening on " + channel)
        self.msg(channel, "Changelog at /msg adventurebot changelog.")

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]

        if user not in self.users:
            try:
                self.users[user] = User.get(username=user)
            except User.DoesNotExist:
                self.users[user] = User.create(username=user)

        if channel in self.input_channels:
            energy = self.engine.process_message(self.users[user], Message(message))
            self.msg(self.output_channel, "{} -- [{}] Line: {} | Total: {}".format(channel, user, energy, self.users[user].energy))
        elif channel == self.nickname:
            i = Interpreter(self, self.engine, self.users[user], message)
            output = i.do_cmd()
            
            for l in output:
                self.msg(user, l)

        # Commit any DB changes incurred.
        self.users[user].save()

    def action(self, user, channel, message):
        yield

    # IRC Callbacks
    def irc_NICK(self, prefix, params):
        old_nick = prefix.split('!')[0]
        new_nick = params[0]
        
        if old_nick in self.users:
            self.users[old_nick].auth = False
            logger.info("%s is now known as %s. Auth status is %s.", 
                old_nick, new_nick, self.users[old_nick].auth)


class ListenerFactory(protocol.ClientFactory):
    def __init__(self, server_settings):
        self.settings = server_settings

    def buildProtocol(self, addr):
        return Listener(self.settings)

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
