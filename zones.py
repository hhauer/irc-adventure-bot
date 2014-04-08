import json
import random

class Zone(object):
    def __init__(self):
        self.name = "A new zone."
        self.mobs = []
        self.level = 0
        self.code = "zone"

    def load(self, code):
        filename = 'zones/' + code

        with open(filename, 'r') as f:
            data = json.load(f)

        self.name = data['name']
        self.mobs = data['mobs']
        self.level = data['level']
        self.code = data['code']
        
    def save(self):
        filename = 'zones/' + self.code
        
        data = {}
        data['name'] = self.name
        data['mobs'] = self.mobs
        data['level'] = self.level
        data['code'] = self.code

        with open(filename, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4, separators=(',',':'))

    def pick_mob(self):
        return (self.level, random.choice(self.mobs))
