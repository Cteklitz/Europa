# Example file showing a circle moving on screen
import pygame
import Assets
import Objects
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player
import random

virtual_res = (176, 142)  # Reduced by 50%
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 10))

player_pos = pygame.Vector2(87.5, 30)  # Reduced by 50%

floor = pygame.image.load("Assets/floor_small.png")
door = pygame.image.load("Assets/powerRoomDoor.png")

locker = Assets.locker
lockerRect = pygame.Rect(50, 19, 32, 64)
lockerInteractRect = pygame.Rect(50, 19, 32, 64)

dimLightScale1 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/4, Assets.squishedDimTiles[1].get_height()*0.75))
dimLightScale2 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/4.4, Assets.squishedDimTiles[1].get_height()*0.75))
dimLightScale3 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/5, Assets.squishedDimTiles[1].get_height()*0.75))

LightScale1 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/4, Assets.squishedTiles[1].get_height()*0.75))
LightScale2 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/4.4, Assets.squishedTiles[1].get_height()*0.75))
LightScale3 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/5, Assets.squishedTiles[1].get_height()*0.75))

class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 1

lights = [
    [Light(78, 90), dimLightScale1, LightScale1],  # Reduced by 50%
    [Light(78, 86), dimLightScale1, LightScale1],
    [Light(78, 82), dimLightScale1, LightScale1],
    [Light(78, 78), dimLightScale1, LightScale1],
    [Light(78, 74), dimLightScale1, LightScale1],
    [Light(78, 70), dimLightScale1, LightScale1],
    [Light(78, 66), dimLightScale1, LightScale1],
    [Light(79, 62), dimLightScale2, LightScale2],
    [Light(80, 58), dimLightScale3, LightScale3]
]

light_pos = (176 / 2, 15)
lightsNew = [LightSource(light_pos[0], light_pos[1], radius=30, strength = 100)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 220)]
circleLight = pygame.image.load("Assets/CircleLight.png")
        
lockerView = False
lights = True

def inBounds(x, y):
    global lockerView

    doorRect = pygame.Rect(150, 24, door.get_width(), door.get_height())  # Reduced by 50%
    if doorRect.collidepoint(x,y):
        if Objects.getBluePower():
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        return 0
    elif lockerView:
        lockerView = False
        return 1
    if y > 134:  # Reduced by 50%
        return False
    if x < 8 or x > 168:  # Reduced by 50%
        return False
    if x < 32:  # Reduced by 50%
        if y > 142 - (x + 32):  # Reduced by 50%
            return True
        return False
    if x >= 32 and x < 144:  # Reduced by 50%
        if y > 78:  # Reduced by 50%
            return True
        return False
    if x >= 144:  # Reduced by 50%
        if y > 142 - (176 - x + 32):  # Reduced by 50%
            return True
        return False

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.PuddleRoom":
        player_pos = pygame.Vector2(150 - 15 + door.get_width()/4, 24 + (door.get_height()*5/6))  # Reduced by 50%
    else:
        player_pos = pygame.Vector2(66, 80)

def Room(screen, screen_res, events):
    global lockerView, lights
    level, power = Objects.getPipeDungeonInfo()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if lockerInteractRect.collidepoint(player_pos):
                    lockerView = True

    # fill the screen with a color to wipe away anything from last frame
    virtual_screen.fill("gray")
    dark_overlay.fill((0, 0, 0, 70))

    pygame.draw.line(virtual_screen, (0,0,0), (31, 0), (31, 78), 1)  # Reduced by 50%
    pygame.draw.line(virtual_screen, (0,0,0), (144, 0), (144, 78), 1)  # Reduced by 50%
    virtual_screen.blit(floor, (0, 78))  # Reduced by 50%

    '''
    if power and level == 2:
        virtual_screen.blit(Assets.tiles[2], (32,0))  # Reduced by 50%
        virtual_screen.blit(Assets.tiles[2], (128,0))  # Reduced by 50%
        virtual_screen.blit(Assets.tiles[2], (32,62))  # Reduced by 50%
        virtual_screen.blit(Assets.tiles[2], (128,62))  # Reduced by 50%
    else:
        virtual_screen.blit(Assets.dimTiles[2], (32,0))  # Reduced by 50%
        virtual_screen.blit(Assets.dimTiles[2], (128,0))  # Reduced by 50%
        virtual_screen.blit(Assets.dimTiles[2], (32,62))  # Reduced by 50%
        virtual_screen.blit(Assets.dimTiles[2], (128,62))  # Reduced by 50%
    '''

    virtual_screen.blit(door, (150,24))  # Reduced by 50%
    virtual_screen.blit(locker, lockerRect)

    Player.animatePlayer(virtual_screen, player_pos)

    # Flickering Lighting
    # determine if lights should start a flicker this frame
    lightRng = random.randint(0, 100)
    if lightRng < 2:
        lights = False

        # play flicker sound
        lightRng = random.randint(1,5)
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

    virtual_screen.blit(circleLight, circleLight.get_rect(center=light_pos))
    # apply lights, make dark if flicker happening
    if (lights):
        apply_lighting(virtual_screen, lightsNew, darkness=60, ambient_color=(20, 20, 20), ambient_strength=10)
        apply_falloff(falloff, virtual_screen, light_pos)
    else:
        dark_overlay.fill((0, 0, 0, 180))

    # determine if light flicker should end this frame
    lightRng = random.randint(0, 100)
    if not lights and lightRng < 30:
        lights = True

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3, 3  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)