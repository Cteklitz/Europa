import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Player
import Items
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Sounds
import random

virtual_res = (250, 150)
virtual_screen = pygame.Surface(virtual_res)
player_pos = pygame.Vector2(192, 128)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

bedNumber = 0 # 0 for left bed, 1 for right bed
exit = False

# load assets
background = Assets.bedBackground

def positionDeterminer(cameFrom):
    pass

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def Room(screen, screen_res, events):
    global exit
    virtual_screen.fill((159, 161, 160))
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    dark_overlay.fill((0, 0, 0, 50))

    bedroom = Objects.getBedroomNumber()
    virtual_screen.blit(background, background.get_rect())

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(f"{bedroom}: {bedNumber}")
                pass

    # location specfic things
    match bedroom:
        case 1: # Bedroom 1
            match bedNumber:
                case 0: # left bed
                    pass
                case 1: # right bed
                    pass
        case 2: # Bedroom 2
            match bedNumber:
                case 0: # left bed
                    pass
                case 1: # right bed
                    pass
        case 3: # Bedroom 3
            match bedNumber:
                case 0: # left bed
                    pass
                case 1: # right bed
                    pass        

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))
    return player_pos, xScale, yScale
