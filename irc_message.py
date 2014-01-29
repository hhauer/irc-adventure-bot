import string

class IRCMessage(object):
    def __init__(self, line):
        tokens = line.split(' ')

        for k in tokens:
            self.tokens = []
            k = k.translate(string.maketrans("", ""), string.punctuation).lower()

            if k != '':
                self.tokens.append(k)

    def is_bot_command(self, bot_name):
        if self.tokens[0] == bot_name:
            return True
        else:
            return False

    def get_tokens(self):
        return self.tokens
