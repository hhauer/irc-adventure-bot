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
        if token not in self.words:
            self.words[token] = 25

        if self.words[token] < 0.01:
            return 0.01

        self.words[token] *= 0.70
        return self.words[token]
