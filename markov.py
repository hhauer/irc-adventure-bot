# Testing out markov chains.
# Based on code from http://pcg.wikidot.com/pcg-algorithm:markov-chain
# http://netlib.bell-labs.com/cm/cs/pearls/sec153.html
import random

class Markov(object):
    def __init__(self, base, order = 2):
        self.table = {}
        self.order = order

        for i in range(len(base) - order):
            try:
                self.table[base[i:i + order]]
            except KeyError:
                self.table[base[i:i + order]] = []

            self.table[base[i:i + order]] += base[i + order]

    def generate(self, start = None, max_length = 12, single_word = False):
        if start == None:
            s = random.choice(self.table.keys())
        else:
            s = start

        try:
            while len(s) < max_length:
                choice = random.choice(self.table[s[-self.order:]])
                if choice == ' ' and single_word is True:
                    return s
                else:
                    s += choice
        except KeyError:
            pass

        return s.strip()

    def print_table(self):
        print self.table

