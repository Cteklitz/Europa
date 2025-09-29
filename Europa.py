# Example file showing a circle moving on screen
import pygame
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# pygame setup
pygame.init()
pygame.mixer.init()

import Area
import Player
import Inventory

# Load player sprites
Player.load_sprites()
from Rooms import ControlRoom, MainRoom, PinkRoom, PinkLowerWing, BookcaseView, OrangeYellow, \
    Safe, PinkUpperWing, TrianglePuzzle, TriangleSolution, BeakerPuzzle, MscopeTable, Microscope, \
    LockedDoor, Desk, Lockbox_puzzle, PinkPower, BlueRoom, Fishtank_puzzle
import Player


import sys

room_dict = {
    "ControlRoom": ControlRoom,
    "MainRoom": MainRoom,
    "PinkRoom": PinkRoom,
    "PinkLowerWing": PinkLowerWing,
    "BookcaseView": BookcaseView,
    "OrangeYellow": OrangeYellow,
    "Safe": Safe,
    "PinkUpperWing": PinkUpperWing,
    "TrianglePuzzle": TrianglePuzzle,
    "TriangleSolution": TriangleSolution,
    "BeakerPuzzle": BeakerPuzzle,
    "MscopeTable": MscopeTable,
    "Microscope": Microscope,
    "LockedDoor": LockedDoor,
    "Desk": Desk,
    "Lockbox_puzzle": Lockbox_puzzle,
    "PinkPower": PinkPower,
    "BlueRoom": BlueRoom,
    "Fishtank_puzzle": Fishtank_puzzle
}

debug_room = None
for i, arg in enumerate(sys.argv):
    if arg == "--debug" and i + 1 < len(sys.argv):
        debug_room = sys.argv[i + 1]
        break

if debug_room and debug_room in room_dict:
    Room = room_dict[debug_room]
else:
    Room = MainRoom  # Default

area = Area.PipeDungeon

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_res = screen.get_size()
clock = pygame.time.Clock()
running = True
dt = 0

def updateRoom(room):
    global Room
    Room = room

while running:
    events = pygame.event.get()
    if Inventory.open:
        Inventory.Inventory(screen, screen_res, events)
    else:
        player_pos, xSpeedScale, ySpeedScale = area.getPos(screen, screen_res, events, Room)
        for event in events:
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_BACKSPACE:
                    check = Room.inBounds(player_pos.x, player_pos.y)
                    if type(check) == int:
                        cameFrom = Room
                        updateRoom(area.getRoom(Room, check))
                        Room.positionDeterminer(cameFrom.__name__)
                if event.key == pygame.K_e:
                    check = Room.inBounds(player_pos.x, player_pos.y)
                    if type(check) == int:
                        cameFrom = Room
                        updateRoom(area.getRoom(Room, check))
                        Room.positionDeterminer(cameFrom.__name__)
                # Open inventory
                if event.key == pygame.K_TAB:
                    Inventory.open = True
                    for item in Player.inventory:
                        print(item)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    check = Room.inBounds(player_pos.x, player_pos.y)
                    if type(check) == int:
                        cameFrom = Room
                        updateRoom(area.getRoom(Room, check))
                        Room.positionDeterminer(cameFrom.__name__)

    keys = pygame.key.get_pressed()
    dx = dy = 0
    
    if keys[pygame.K_w]:
        y = player_pos.y - 325 * dt / ySpeedScale
        check = Room.inBounds(player_pos.x, y)
        if type(check) == int:
            cameFrom = Room
            updateRoom(area.getRoom(Room, check))
            Room.positionDeterminer(cameFrom.__name__)
        elif check:
            player_pos.y = y
            dy = -1
    if keys[pygame.K_s]:
        y = player_pos.y + 325 * dt / ySpeedScale
        check = Room.inBounds(player_pos.x, y)
        if type(check) == int:
            cameFrom = Room
            updateRoom(area.getRoom(Room, check))
            Room.positionDeterminer(cameFrom.__name__)
        elif check:
            player_pos.y = y
            dy = 1
    if keys[pygame.K_a]:
        x = player_pos.x - 325 * dt / xSpeedScale
        check = Room.inBounds(x, player_pos.y)
        if type(check) == int:
            cameFrom = Room
            updateRoom(area.getRoom(Room, check))
            Room.positionDeterminer(cameFrom.__name__)
        elif check:
            player_pos.x = x
            dx = -1
    if keys[pygame.K_d]:
        x = player_pos.x + 325 * dt / xSpeedScale
        check = Room.inBounds(x, player_pos.y)
        if type(check) == int:
            cameFrom = Room
            updateRoom(area.getRoom(Room, check))
            Room.positionDeterminer(cameFrom.__name__)
        elif check:
            player_pos.x = x
            dx = 1
            
    # Update player animation state
    Player.update_movement(dx, dy)

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