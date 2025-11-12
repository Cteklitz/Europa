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
lightsOn = True

# load assets
backgroundLeft = Assets.bedBackgroundLeft
backgroundRight = Assets.bedBackgroundRight

radioOn = Assets.radioOn
radioOff = Assets.radioOff

def positionDeterminer(cameFrom):
    pass

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def Room(screen, screen_res, events):
    global exit, lightsOn
    virtual_screen.fill((159, 161, 160))
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    # Add greenpower statement
    if level == 3 and power:
        greenPowerOn = True
    else:
        greenPowerOn = False
    #greenPowerOn = True # FOR TESTING

    dark_overlay.fill((0, 0, 0, 100))

    bedroom = Objects.getBedroomNumber()
    if bedNumber == 0:
        virtual_screen.blit(backgroundLeft, backgroundLeft.get_rect())
    else:
        virtual_screen.blit(backgroundRight, backgroundRight.get_rect())

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
            lightsOn = True

            match bedNumber:
                case 0: # left bed
                    pass
                case 1: # right bed
                    pass
        case 2: # Bedroom 2
            # light flickering
            lightRng = random.randint(0, 100)
            if lightRng < 2:
                lightsOn = False

                # play flicker sound
                lightRng = random.randint(1,5)
                if greenPowerOn:
                    match lightRng:
                        case 1:
                            Sounds.spark1.play()
                        case 2:
                            Sounds.spark2.play()
                        case 3:
                            Sounds.spark3.play()
                        case 4:
                            Sounds.spark4.play()
                        case 5:
                            Sounds.spark5.play()

            match bedNumber:
                case 0: # left bed
                    if greenPowerOn:
                        virtual_screen.blit(radioOn, (97,94))
                    else:
                        virtual_screen.blit(radioOff, (97,94))
                case 1: # right bed
                    pass
        case 3: # Bedroom 3
            lightsOn = True

            match bedNumber:
                case 0: # left bed
                    pass
                case 1: # right bed
                    pass        

    if not greenPowerOn:
        lightsOn = False

    if not lightsOn:
        virtual_screen.blit(dark_overlay, (0, 0))

    lightRng = random.randint(0, 100)
    if not lightsOn and lightRng < 30:
        lightsOn = True

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))
    return player_pos, xScale, yScale
