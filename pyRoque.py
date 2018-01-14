
import re
from collections import namedtuple

class MoneyType:
    def __init__(self, name, worth, weight):
        self.name = name
        self.worth = worth
        self.weight = weight
    
    def __repr__(self):
        return "%s %s %s" % (self.name, self.worth, self.weight)

EnvType = namedtuple("EnvType", "name, value")

# Define types of coins
MoneyTypes = [
    MoneyType("platinum", 10.0, 0.01),
    MoneyType("gold", 1.0, 0.01),
    MoneyType("silver", 0.6, 0.01),
    MoneyType("bronze", 0.4, 0.01),
    MoneyType("copper", 0.2, 0.01),
    MoneyType("wood", 0.01, 0.01)
]

# Define types of tunnels
EnvTypes = [
    EnvType("dark", 0.0),
    EnvType("tall", 0.0),
    EnvType("humid", 0.0),
    EnvType("beautiful", 0.0),
    EnvType("narrow", 0.0)
]


def main():
    print ("Welcome to the treasure dungeon")
    
    # the main loop
    # Look()
    while(life > 0) {
        # Produce the prompt and wait for player's command
        s = input("%s", life)

        if (s == "") continue

        if (re.match())
    }

if __name__ == "__main__": main()