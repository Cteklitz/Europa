import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon

virtual_res = (389, 189)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

# Item positions and scales
mop_pos = (44, 94)
mop_scale = 0.6
tape_pos = (54, 26)
tape_scale = 0.2

# Load images
lockerViewBg = pygame.image.load("Assets/LockerView.png")
mop = pygame.image.load("Assets/Mop.png")
yellowElectricalTape = pygame.image.load("Assets/YellowElectricalTape.png")

exit = False

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def LockerView(screen, screen_res, events):
    global exit
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                exit = True

    # Display background image
    virtual_screen.blit(lockerViewBg, (0, 0))

    scaled_mop = pygame.transform.scale(mop, (int(mop.get_width() * mop_scale), int(mop.get_height() * mop_scale)))
    scaled_tape = pygame.transform.scale(yellowElectricalTape, (int(yellowElectricalTape.get_width() * tape_scale), int(yellowElectricalTape.get_height() * tape_scale)))
    
    virtual_screen.blit(scaled_mop, mop_pos)
    virtual_screen.blit(scaled_tape, tape_pos)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale