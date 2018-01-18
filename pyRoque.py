import sys
import click
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
class Room:
    def __init__(self):
        self.Wall = 0
        self.Env = 0
        self.Seed = 0

 

# Player's location and life
x = 0
y = 0
life = 100

def Look():
    click.echo("You see nothing")

def Eat():
    click.echo('Nothing to eat')    

def TryMoveBy(x,y):
    return True

def Help():
    click.echo("Available commands:")
    click.echo("\tw/a/s/d for moving")
    click.echo("\th = help")
    click.echo("\tq = quit")
    click.echo("Everywhere are Zombies, they come after you.")
    click.echo("Try to find the helicopter before you are dead.")
    click.echo("\n\n")

def Quit():
    click.echo("You killed yourself.")
    sys.exit(1)


def main():
    click.echo("Welcome to the zombie city, try to find the helicopter to escape.")
    
    # the main loop
    Look()
    while(life > 0):
        # Produce the prompt and wait for player's command
        click.echo('[%s]>' % life)
        key = click.getchar()

        if key == 'h': Help()
        if key == 'w' and TryMoveBy( 0, -1): Look()                  
        if key == 'a' and TryMoveBy(-1,  0): Look()
        if key == 's' and TryMoveBy( 0,  1): Look()
        if key == 'd' and TryMoveBy( 1,  0): Look()
        if key == 'e': Eat()
        if key == 'q': Quit()

    click.echo('You have died.')

if __name__ == "__main__":
    main()