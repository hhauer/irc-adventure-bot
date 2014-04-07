import json
import random

class Zone(object):
    def __init__(self):
        self.name = "A new zone."
        self.mobs = []
        self.level = 0

    def load(self, name):
        filename = 'zones/' + name

        with open(filename, 'r') as f:
            data = json.load(f)

        self.name = data['name']
        self.mobs = data['mobs']
        self.level = data['level']
        
    def save(self, name):
        filename = 'zones/' + name
        
        data = {}
        data['name'] = self.name
        data['mobs'] = self.mobs
        data['level'] = self.level

        with open(filename, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',',':'))

    def pick_mob(self):
        return (self.level, random.choice(self.mobs))
