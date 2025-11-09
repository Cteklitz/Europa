# Example file showing a circle moving on screen
import pygame
import os

scriptDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptDir)

# pygame setup
pygame.init()
pygame.mixer.init()


import Area
from Rooms import MainRoom
import Player
import Inventory

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screenRes = screen.get_size()
clock = pygame.time.Clock()
running = True
dt = 0
area = Area.PipeDungeon
Room = MainRoom

# Each room file must contain these three functions:
# 1. Room(screen, screen_res, events) - Contains the loop of what is being drawn for that room, logic to update variables based on input, etc.
#    Its parameters are passed to it from this file (the main game loop) through Area.py's getPos().
#
# 2. inBounds(x, y) - Serves two purposes:
#       1. When within a room, it returns a bool True or False. This defines the bounding box for where the player can walk.
#
#       2. When the given position results in a room change (often a position that collides with a door) it returns an int number code. 
#       This code corresponds with an index for that room's array of connected rooms within the roomLayout of that room's Area (see Area.py)
#
# 3. positionDeterminer(cameFrom) - Only called after a room update. Sets the initial position of player in the new room based on room the player came from.
#    Isn't always explicitly needed (ie. for screens where you aren't moving the player). In these cases leaving just 'pass' in the body is acceptable.

def updateRoom(room):
    global Room
    Room = room

while running:
    events = pygame.event.get()
    if Inventory.open:
        Inventory.Inventory(screen, screenRes, events)
    else:
        player_pos, xSpeedScale, ySpeedScale = area.getPos(screen, screenRes, events, Room)

        for event in events:
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Open inventory
                if event.key == pygame.K_TAB:
                    Inventory.open = True
                    for item in Player.inventory:
                        print(item)

        #Movement
        keys = pygame.key.get_pressed()
        x = player_pos.x
        y = player_pos.y
        Player.moving = False
        if keys[pygame.K_s]:
            Player.down = True
            y = y + 250 * dt / ySpeedScale
            Player.moving = True
        else:
            Player.down = False
        if keys[pygame.K_a]:
            Player.left = True
            Player.right = False
            x = x - 250 * dt / xSpeedScale
            Player.moving = True
        if keys[pygame.K_d]:
            Player.left = False
            Player.right = True
            x = x + 250 * dt / xSpeedScale
            Player.moving = True
        if keys[pygame.K_w]:
            Player.up = True
            y = y - 250 * dt / ySpeedScale
            Player.moving = True
        elif Player.moving:
            Player.up = False

        #Checks if horizontal movement results in room change. If so, update the room to new room and set the initial position with positionDeterminer
        check = Room.inBounds(x, player_pos.y)
        if type(check) == int:
            cameFrom = Room
            updateRoom(area.getRoom(Room, check))
            Room.positionDeterminer(cameFrom.__name__)
        else:
            if check:
                player_pos.update(x, player_pos.y)

            #Checks if vertical movement results in room change. If so, update the room to new room and set the initial position with positionDeterminer
            check = Room.inBounds(player_pos.x, y)
            if type(check) == int:
                cameFrom = Room
                updateRoom(area.getRoom(Room, check))
                Room.positionDeterminer(cameFrom.__name__)
            elif check:
                player_pos.update(player_pos.x, y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()