import string

class IRCUser(object):
    def __init__(self, username):
        self.username = username
        self.lines = 0
        self.words = {}

    def analyze(self):
        print "{} said {} lines.".format(self.username, self.lines)
        print "Word breakdown: "

        for k, v in self.words.items():
            print "{}: {}".format(k, v)

    def parse_line(self, line):
        self.lines += 1
        tokens = line.split(' ')

        for k in tokens:
            k = k.translate(string.maketrans("",""), string.punctuation).lower()

            if k not in self.words:
                self.words[k] = 1
            else:
                self.words[k] += 1
