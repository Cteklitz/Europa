# Example file showing a circle moving on screen
import pygame
import os

scriptDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(scriptDir)

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
    LockedDoor, Desk, Lockbox_puzzle, PinkPower, BlueRoom, Fishtank_puzzle, SpotDiffs
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
    "Fishtank_puzzle": Fishtank_puzzle,
    "SpotDiffs": SpotDiffs
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
screenRes = screen.get_size()
clock = pygame.time.Clock()
running = True
dt = 0

def updateRoom(room):
    global Room
    Room = room

# Import debugging module
from Debugging.debug_system import debug_system

while running:
    events = pygame.event.get()
    
    # Handle debug teleportation
    if hasattr(debug_system, 'teleport_target') and debug_system.teleport_target:
        target_room = debug_system.teleport_target
        debug_system.teleport_target = None  # Reset the target
        
        # Update to the target room
        if target_room in room_dict:
            updateRoom(room_dict[target_room])
            Room.positionDeterminer("Debug")
    
    if debug_system.panel_open:
        debug_system.draw_panel(screen, screenRes, events)
    elif Inventory.open:
        Inventory.Inventory(screen, screenRes, events)
    else:
        playerPos, xSpeedScale, ySpeedScale = area.getPos(screen, screenRes, events, Room)

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
                # Debug menu
                if event.key == pygame.K_h:
                    debug_system.toggle_panel()

        #Movement
        keys = pygame.key.get_pressed()
        dx, dy = Player.handle_movement(keys, dt, playerPos, ySpeedScale, xSpeedScale, Room, area, updateRoom)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()