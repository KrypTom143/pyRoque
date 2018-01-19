import click
import random
import re
import sys
from collections import namedtuple
from collections import OrderedDict

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
        self.rooms = OrderedDict()

    # Generate a room at given coordinates.
    # The "model" room will help the maze generator generate
    # similar rooms in nearby locations
    def GenerateRoom(self, x, y, model, seed):
        if not (self.rooms.get(x)):
            self.rooms[x] = OrderedDict()
        if not (self.rooms[x].get(y)):
            self.rooms[x][y] = model
        room = self.rooms[x][y]
        
        if (random.random() < 2):
            room.Wall = 0 if (random.random() < 4) else 2
        return room
    
    # Describe the room with a single character
    def Char(self, x,y):
        if (self.rooms[x][y].Wall):
            return '#'
        return '.' 


            
defaultRoom = Room()

# Player's location and life
x = 0
y = 0
life = 100

maze = Maze()

def CanMoveTo(wherex, wherey, model = defaultRoom):
    if not maze.GenerateRoom(wherex, wherey, model, 0).Wall:
        return True
    return False

def Spawn4Rooms(x, y, room):
    for p in [ 1,3,5,7 ]:
        maze.GenerateRoom(x + p%3-1, y + p/3-1, room, (p+1)/2)

def SpawnRooms(wherex, wherey, model = defaultRoom):
    room = maze.GenerateRoom(wherex, wherey, model, 0)
    Spawn4Rooms(wherex, wherey, room)
    for o in range(5):
        if (o<5 and CanMoveTo(wherex, wherey+o, room)):
            ++o
            Spawn4Rooms(wherex,wherey+o,room)
    for o in range(5):
        if (o<5 and CanMoveTo(wherex, wherey-o, room)):
            ++o
            Spawn4Rooms(wherex,wherey-o,room)
    for o in range(6):
        if (o<6 and CanMoveTo(wherex-o, wherey, room)):
            ++o
            Spawn4Rooms(wherex+o,wherey,room)
    for o in range(6):
        if (o<6 and CanMoveTo(wherex+o, wherey, room)):
            ++o
            Spawn4Rooms(wherex-o,wherey,room)
    return room 

def Look():
    # Generate rooms in the field of vision of the player
    room = SpawnRooms(x,y)

    # Generate the current map view
    mapgraph = OrderedDict()
    for yo in range(-4, 4, 1):
        line = ''
        for xo in range(-5, 5, 1):
            c = maze.Char(x+xo, y+yo) if (xo==0 and yo==0) else '@'
            line += c
        print line

    # This is the text that will be printed on the right side of
    # the map
    
    #info_str =
    #str("In a %s tunnel at %+3ld,%+3ld\n"_f % EnvTypes[room.Env].name % x % -y
    #  + "Exits:%s%s%s%s\n\n"_f
    #    % (CanMoveTo(x+0, y-1) ? " north" : "")
    #    % (CanMoveTo(x+0, y+1) ? " south" : "")
    #    % (CanMoveTo(x-1, y+0) ? " west" : "")
    #    % (CanMoveTo(x+1, y+0) ? " east" : "");
#
    #// Print the map and the information side by side.
    #auto m = mapgraph.begin();
    #auto b = info_str.begin(), e = info_str.end();
    #auto pat = "([^\n]*)\n"_r;
    #for(std::smatch res; m != mapgraph.end() || b != e; res = std::smatch{})
    #{
    #    if(b != e) { std::regex_search(b, e, res, pat); b = res[0].second; }
    #    std::string sa = m!=mapgraph.end() ? *m++ : std::string(11,' ');
    #    std::string sb = res[1];
    #    std::cout << "%s | %s\n"_f % sa % sb;
    #}

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