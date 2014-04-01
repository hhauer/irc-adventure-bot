from datetime import datetime, timedelta

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
        energy = 25

        if token not in self.words:
            self.words[token] = {
                    'energy': energy,
                    'last_used': datetime.now(),
                    }
        else:
            scale = self.energy_scale(self.words[token]['last_used'], datetime.now())
            energy = self.words[token]['energy'] * scale

        if energy < 1:
            energy = 1

        self.words[token]['energy'] = energy
        return energy

    def energy_scale(self, last, current):
        delta = current - last

        # 60s * 60m = 1hr
        scale = delta.total_seconds() / (60 * 60)

        if scale > 12:
            return 12
        elif scale < 0.05:
            return 0.1
        else:
            return scale
