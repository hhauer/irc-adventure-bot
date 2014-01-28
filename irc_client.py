# http://twistedmatrix.com/documents/current/words/examples/ircLogBot.py

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol

from irc_user import IRCUser

class GameListener(irc.IRCClient):
    nickname = 'AdventureBot'
    realname = 'omghai'
    username = 'Bot'
    lineRate = 1

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.join('informationsociety')

        self.users = {}

    def privmsg(self, user, channel, message):
        user = user.split('!', 1)[0]

        if user not in self.users:
            self.users[user] = IRCUser(user)

        self.users[user].parse_line(message)
        self.users[user].analyze()

class GameListenerFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return GameListener()

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason
        reactor.stop()

if __name__ == '__main__':
    f = GameListenerFactory()
    reactor.connectTCP("irc.cat.pdx.edu", 6667, f)
    reactor.run()
