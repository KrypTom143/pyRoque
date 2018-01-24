import click
import random
import re
import sys
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

class Maze:
    # A maze contains rooms
    def __init__(self):
        self.rooms = dict()

    # Generate a room at given coordinates.
    # The "model" room will help the maze generator generate
    # similar rooms in nearby locations
    def GenerateRoom(self, x, y, model, seed):
        random.seed(x * 3.141 + y * 19820000000)

        if not (x in self.rooms):
            self.rooms[x] = dict()
        if not (y in self.rooms[x]):
            if (random.random() < .4):
                model.Wall = 2 if (random.random() < 0.4) else 0
            self.rooms[x][y] = model
            #click.echo("Created({},{})".format(x,y))
        
        return self.rooms[x][y]
    
    # Describe the room with a single character
    def Char(self, x, y):
        try:
            if not (x in self.rooms) and not (y in self.rooms[x]):
                return '_'
            else:
                return '#' if (self.rooms[x][y].Wall) else '.'
        except KeyError as err:
            click.echo("Fail: {}".format(err))
        return ' '

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.life = 100

    def EatLife(self, l):
        msg = ''
        if (self.life >= 800 and self.life-l<800):
            msg = 'You are so hungry!'
        if (self.life >= 150 and self.life-l<150):
            msg = 'You are famished!'
        if (self.life >= 70 and self.life-l<70):
            msg = 'You are about to collapse any second'
        self.life -= l
        if (msg):
            click.echo(msg)  


def CanMoveTo(wherex, wherey, model = Room()):
    if not maze.GenerateRoom(wherex, wherey, model, 0).Wall:
        return True
    return False

def Spawn4Rooms(wherex, wherey, room = Room()):
    # click.echo("Spawn4Rooms({},{})".format(x,y))
    for px in range(wherex-5, wherey+5, 1):
        for py in range(wherex-5, wherey+5, 1):
            maze.GenerateRoom(px, py, room, px*py)

def SpawnRooms(wherex, wherey, model = Room()):
    # click.echo("SpawnRooms({},{})".format(x,y))
    room = maze.GenerateRoom(wherex, wherey, model, 0)
    Spawn4Rooms(wherex, wherey)

    for o in range(1,5,1):
        Spawn4Rooms(wherex, wherey+o, room)
        Spawn4Rooms(wherex, wherey-o, room)
    for o in range(1,6,1):
        Spawn4Rooms(wherex-o, wherey, room)
        Spawn4Rooms(wherex+o, wherey, room)
    return room 

def Look():
    # Generate rooms in the field of vision of the player
    room = SpawnRooms(player.x, player.y)

    # Generate the current map view
    for yo in range(-5, 5, 1):
        line = ''
        for xo in range(-4, 4, 1):
            line += '@' if (xo==0 and yo==0) else maze.Char(player.x + xo, player.y + yo)
        click.echo(line)

  

def TryMoveBy(xd, yd):
    click.echo("{},{}".format(player.x, player.y))
    # If we are moving diagonally, ensure that there is an actual path.
    if not CanMoveTo(player.x + xd, player.y + yd) or not CanMoveTo(player.x, player.y + yd) and not CanMoveTo(player.x + xd, player.y):
        click.echo("You cannot go that way.")
        return False
    player.x += xd
    player.y += yd
    player.EatLife(1)
    return True

def Help():
    click.echo("Available commands:")
    click.echo("\tw/a/s/d for moving")
    click.echo("\th = help")
    click.echo("\tq = quit")
    click.echo("Everywhere are Zombies, they come after you.")
    click.echo("Try to find the helicopter before you are dead.")
    click.echo("\n\n")
    click.echo("You are at [{},{}]".format(x,y))
    click.echo("Life: {}".format(life))
    click.echo("\n\n")

def Quit():
    click.echo("You killed yourself.")
    sys.exit(1)



maze = Maze()
player = Player()

def Main():
    click.echo("Welcome to the zombie city.")
    click.echo("try to find the helicopter to escape.")
    # the main loop
    Look()
    while(player.life > 0):
        # Produce the prompt and wait for player's command
        click.echo("[{},{}    {}]>".format(player.x, player.y, player.life))
        key = click.getchar()

        if key == 'h':
            Help()
        if key == 'w' and TryMoveBy(0, -1):
            Look()                  
        if key == 'a' and TryMoveBy(-1, 0):
            Look()
        if key == 's' and TryMoveBy(0, 1):
            Look()
        if key == 'd' and TryMoveBy(1, 0):
            Look()
        if key == 'e':
            player.EatLife(1)
        if key == 'q':
            Quit()

    click.echo('You have died.')

if __name__ == "__main__":
    try:
        Main()
    except:
        print("Unexpected error: %s" % sys.exc_info()[0])
        raise