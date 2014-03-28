import string

class IRCMessage(object):
    def __init__(self, line):
        line = line.translate(string.maketrans('', ''), string.punctuation).lower()
        self.tokens = line.split()

    def next_token(self):
        return self.tokens.pop(0)
