from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from game import Engine

class User(object):
    def __init__(self, username):
        self.username = username
        self.energy = 0.00

class Message(object):
    def __init__(self, line):
        #line = line.translate(string.maketrans('', ''), string.punctuation).lower()
        self.tokens = line.lower().split()

class Listener(irc.IRCClient):
    nickname = 'AdventureBot'
    realname = 'AdventureBot'
    username = 'AdventureBot'
    linerate = 1

    engine = Engine()

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.join('informationsociety')

        self.users = {}

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]

        if user not in self.users:
            self.users[user] = User(user)

        energy = self.engine.process_message(self.users[user], Message(message))
        self.msg(channel, "{}: that line was worth {} energy for a total of {}.".format(user, energy, self.users[user].energy))

class ListenerFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Listener()

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()

# Test stub.
if __name__ == '__main__':
    f = ListenerFactory()
    reactor.connectTCP("irc.cat.pdx.edu", 6667, f)
    reactor.run()
