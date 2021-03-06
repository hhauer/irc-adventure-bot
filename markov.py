# Testing out markov chains.
# Based on code from http://pcg.wikidot.com/pcg-algorithm:markov-chain
# http://netlib.bell-labs.com/cm/cs/pearls/sec153.html
import random

class Markov(object):
    def __init__(self, words, order = 2):
        self.table = {}
        self.order = order

        for w in words:
            w = w.encode('ascii', 'ignore')

            for i in range(len(w) - order):
                if w[i:i + order] not in self.table:
                    self.table[w[i:i + order]] = []

                self.table[w[i:i + order]] += w[i + order]

    def generate(self, start = None, max_length = 20):
        s = start or random.choice(self.table.keys())

        length = random.randrange(4, max_length)
        try:
            while len(s) < max_length:
                s += random.choice(self.table[s[-self.order:]])

        except KeyError:
            pass

        return s.strip()

    def print_table(self):
        print self.table

