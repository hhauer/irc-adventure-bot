from datetime import datetime, timedelta
import json
import cPickle
import copy

# Logging
import logging
logger = logging.getLogger(__name__)

class Engine(object):
    def __init__(self):
        self.words = {}

    def process_message(self, user, message):
        score = 0

        for t in message.tokens:
            score += self.token_value(t)

        user.energy += score
        return score

    def token_value(self, token):
        energy = 10

        if token not in self.words:
            self.words[token] = {
                    'last_used': datetime.now(),
                    'times': 1,
                    }
        else:
            scale = self.energy_scale(self.words[token]['last_used'], datetime.now())
            energy *= scale
            self.words[token]['times'] += 1
            logger.debug("[{}] Scale: {} | Energy: {}".format(token, scale, energy))

        if energy < 1:
            energy = 1

        return energy

    def energy_scale(self, last, current):
        delta = current - last

        # 60s * 60m = 1hr
        hours = delta.total_seconds() / (60 * 60)

        # Magic numbers from a regression analysis based on:
        # fit {{0, 0}, {1, 0.2}, {2, 0.5}, {3, 0.9}, {24, 10}}
        scale = 0.425122 * hours - 0.230732

        if scale > 10:
            return 10
        elif scale < 0.1:
            return 0.1
        else:
            return scale
