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
        if keys[pygame.K_w]:
            y = player_pos.y - 325 * dt / ySpeedScale
            #Checks if the movement upwards results in room change. If so, update the room to new room and set the initial position with positionDeterminer
            check = Room.inBounds(player_pos.x, y)
            if type(check) == int:
                cameFrom = Room
                updateRoom(area.getRoom(Room, check))
                Room.positionDeterminer(cameFrom.__name__)
            elif check:
                player_pos.y = y
        if keys[pygame.K_s]:
            y = player_pos.y + 325 * dt / ySpeedScale
            #Checks if the movement downwards results in room change. If so, update the room to new room and set the initial position with positionDeterminer
            check = Room.inBounds(player_pos.x, y)
            if type(check) == int:
                cameFrom = Room
                updateRoom(area.getRoom(Room, check))
                Room.positionDeterminer(cameFrom.__name__)
            elif check:
                player_pos.y = y
        if keys[pygame.K_a]:
            x = player_pos.x - 325 * dt / xSpeedScale
            #Checks if the movement to the left results in room change. If so, update the room to new room and set the initial position with positionDeterminer
            check = Room.inBounds(x, player_pos.y)
            if type(check) == int:
                cameFrom = Room
                updateRoom(area.getRoom(Room, check))
                Room.positionDeterminer(cameFrom.__name__)
            elif check:
                player_pos.x = x
        if keys[pygame.K_d]:
            x = player_pos.x + 325 * dt / xSpeedScale
            #Checks if the movement to the right results in room change. If so, update the room to new room and set the initial position with positionDeterminer
            check = Room.inBounds(x, player_pos.y)
            if type(check) == int:
                cameFrom = Room
                updateRoom(area.getRoom(Room, check))
                Room.positionDeterminer(cameFrom.__name__)
            elif check:
                player_pos.x = x

        #Checks if any other input (mouse click, backspace, etc.) results in room change. If so, update the room to new room and set the initial position with positionDeterminer
        check = Room.inBounds(player_pos.x, player_pos.y)
        if type(check) == int:
            cameFrom = Room
            updateRoom(area.getRoom(Room, check))
            Room.positionDeterminer(cameFrom.__name__)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()