from zones import Zone
import json

zone_list = []

z = Zone()
z.name = "Werewolf Bar Mitzvah, Spooky Scary"
z.mobs = [
    "Rabbi Wolfstein",
    "Orthodox Werewolf",
    "Unorthodox Werewolf",
    "Seven Well-Behaved Wolfpups, why not?",
    "Murray",
]
z.level = 5
z.code = 'werewolves'
z.save()

zone_list.append(z.code)

z = Zone()
z.name = "The Briny Deeps"
z.mobs = [
    "Brine Shrimp",
    "Brine Sodium",
    "Brine Chloride",
]
z.level = 3
z.code = 'brine'
z.save()

zone_list.append(z.code)

z = Zone()
z.name = "Obligatory Den Of Easily Overcome Mice"
z.mobs = [
    "A mouse",
    "A mice",
    "Some mouse",
    "Some mice",
    "Meese?",
    "Moose? ...",
    "Maps? Now it's not even making sense anymore.",
]
z.level = 1
z.save()

zone_list.append(z.code)

with open('zones/index', 'w') as f:
    json.dump(zone_list, f)

