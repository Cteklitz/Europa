import pygame
import Assets
import Objects
import Items
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player
import random

virtual_res = (648,357)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_res2 = (400, 219)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay2 = pygame.Surface(virtual_screen2.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(239, 180)

fertilizer = pygame.image.load("Assets/Fertilizer.png")
fertilizer_pos = (20, 90)

rake = pygame.image.load("Assets/Rake.png")
rake_pos = (45, 75)

waterCan = pygame.image.load("Assets/WaterCan.png")
waterCan_pos = (15, 120)

eyeOpen = pygame.transform.scale(pygame.image.load("Assets/EyeWall.png"), (120, 85))
eyeClosed = pygame.transform.scale(pygame.image.load("Assets/eyeClosedWall.png"), (120, 85))

eyeOpenSmall = pygame.transform.scale(pygame.image.load("Assets/EyeWall.png"), (30, 22))
eyeClosedSmall = pygame.transform.scale(pygame.image.load("Assets/eyeClosedWall.png"), (30, 22))

eye_rect = pygame.Rect(0, 0, eyeOpen.get_width(), 100)
eye_rect2 = pygame.Rect(0, 0, 30, 22)

eyes = [eyeOpen, eyeClosed]
eyes2 = [eyeOpenSmall, eyeClosedSmall]
currEye = eyes[0]
currEye2 = eyes2[1]
currIndex = 0
currIndex2 = 0

added = False

smallEyesPositions = [
    (231, 40),
    (261, 91),
    (261, 141),
    (231, 177),
    (113, 177),
    (83, 141),
    (83, 91),
    (113, 40),
    (204, 53),      
    (237, 118),     
    (204, 168),     
    (140, 168), 
    (107, 118),
    (140, 53),
    (172, 72),
    (172, 151)
]

firstTime = pygame.time.get_ticks()
firstTime2 = pygame.time.get_ticks()
nextBlinkDelay = random.randint(3000, 5000)
nextBlinkDelay2 = random.randint(3000, 5000)
bounds = Polygon([(32,224),(0,287),(227,280),(453,247),(453,224)])

lit = False
light_pos = (70, 50)
light_pos2 = (240, 50)
wall_lights = [
    LightSource(light_pos[0], light_pos[1], radius=60, strength = 220),
    LightSource(light_pos2[0], light_pos2[1], radius=60, strength = 220)
]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

# load assets
background = pygame.image.load("Assets/SubRoom.png")
exitRect = pygame.Rect(4, 175, 21, 115)

def inBounds(x, y):
    if exitRect.collidepoint((x,y)):
        Sounds.whispers.stop()
        return 0
    elif not bounds.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos, added
    if not added:
        Player.events += 1
        added = True
    if cameFrom == "Rooms.YellowHallway":
        Sounds.whispers.play(-1)
        player_pos = pygame.Vector2(exitRect.centerx + 35, exitRect.centery + 25)

def Room(screen, screen_res, events):
    global firstTime, currIndex, nextBlinkDelay, currEye, firstTime2, currIndex2, currEye2, nextBlinkDelay2, smallEyesPositions
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()


    currTime = pygame.time.get_ticks()
    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:
    
    virtual_screen.blit(background, (0,0))


    if (currTime - firstTime2 >= nextBlinkDelay2):
            currIndex2 = (currIndex2 + 1) % len(eyes2)
            currEye2 = eyes2[currIndex2] # sets current eye for animation in array
            firstTime2 = currTime
            if currIndex2 == 1: # closed eye
                nextBlinkDelay2 = random.randint(70, 120)
                Sounds.blink.play()
            else: # open eye
                nextBlinkDelay2 = random.randint(2000, 5000)
    for position in smallEyesPositions:    
        virtual_screen.blit(currEye2, position, eye_rect2)

    if (currTime - firstTime >= nextBlinkDelay):
        currIndex = (currIndex + 1) % len(eyes)
        currEye = eyes[currIndex] # sets current eye for animation in array
        firstTime = currTime
        if currIndex == 1: # closed eye
            nextBlinkDelay = random.randint(70, 120)
            Sounds.blink.play()
        else: # open eye
            nextBlinkDelay = random.randint(2000, 5000)
    virtual_screen.blit(currEye, (130, 80), eye_rect)           

    Player.animatePlayer(virtual_screen, player_pos)

    apply_lighting(virtual_screen, wall_lights, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    apply_falloff(falloff, virtual_screen, light_pos)

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3.5, 3.5  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
