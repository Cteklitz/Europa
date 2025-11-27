import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player
import math
import Items

virtual_res = (640, 260)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_view_res = (virtual_screen.get_width()/2, virtual_screen.get_height())

player_pos = pygame.Vector2(192, 128)

lights = [
    Objects.SquishedLight(0, 113, 4),
    Objects.SquishedLight(208, 113, 4),
    Objects.SquishedLight(400, 113, 4),
    Objects.SquishedLight(604, 113, 4)
]

# New Lighting
greenLightRadius = 25
greenLightStrength = 100
#pinkLightColor = (245, 118, 238)
greenLightColor = (181, 230, 29)
ambientLightPos = (256/2, 256/2)
lightsNew = [LightSource(ambientLightPos[0], ambientLightPos[1], radius=60, strength = 200),
             LightSource(lights[0].x + 16, lights[0].y + 16, radius=greenLightRadius, strength = greenLightStrength, color = greenLightColor),
             LightSource(lights[1].x + 16, lights[1].y + 16, radius=greenLightRadius, strength = greenLightStrength, color = greenLightColor)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 50)]
falloffPartial = [LightFalloff(virtual_screen.get_size(), darkness = 75)]

exitDoorImg = pygame.transform.scale(Assets.grayDoorSouth, (75,75))
ValveDoor = pygame.image.load("Assets/ValveDoor.png")
MissingValveDoor = pygame.image.load("Assets/MissingValveDoor.png")
window = pygame.transform.scale(pygame.image.load("Assets/EmptyWindow.png"), (125, 55))
ValveDoor1 = Objects.Door(88, 48, ValveDoor)
ValveDoor2 = Objects.Door(288, 48, ValveDoor)
ValveDoor3 = Objects.Door(488, 48, MissingValveDoor)
exitDoor = Objects.Door(283, 161, exitDoorImg)

unlocked = False

# outer rect
outerRect = pygame.Rect(0,0,640,240)
# inner rect
innerRect = pygame.Rect(0,112,640,50)

def inBounds(x, y):
    global unlocked
    level, power = Objects.getPipeDungeonInfo()
    bounds = pygame.Rect(innerRect.x+32,innerRect.y-8, innerRect.width-64,innerRect.height-4)
    exitWalkRect = pygame.Rect(exitDoor.x, exitDoor.y - 20, exitDoor.rect.width, exitDoor.rect.height)
    # Add greenpower statement
    if (level == 3 and power) or Objects.getGreenPower():
        greenPowerOn = True
    else:
        greenPowerOn = False
    #greenPowerOn = True # FOR TESTING

    if exitDoor.rect.collidepoint((x,y)):
        return 0
    elif ValveDoor3.rect.collidepoint((x,y)):
        Sounds.radioFar.set_volume(0)
        Sounds.radioClose.set_volume(0)
        return 1
    elif exitWalkRect.collidepoint((x,y)):
        return True
    elif not bounds.collidepoint((x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos

    if cameFrom == "Rooms.YellowRoom":    
        player_pos = pygame.Vector2(exitDoor.x + exitDoor.rect.width/2, exitDoor.y - 5)
    elif cameFrom == "Rooms.SubRoom":
        player_pos = pygame.Vector2(ValveDoor3.x + ValveDoor3.rect.width/2, ValveDoor3.y + 69)

def Room(screen, screen_res, events):
    global player_pos, unlocked
    level, power = Objects.getPipeDungeonInfo()

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = event.pos
            click_x_unscaled = click_x/xScale
            click_y_unscaled = click_y/yScale
            print(click_x_unscaled, click_y_unscaled)
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    pygame.draw.rect(virtual_screen, "gray", outerRect)
    pygame.draw.rect(virtual_screen, "black", outerRect, 1)
    pygame.draw.rect(virtual_screen, "black", innerRect, 1)

    Done = False

    for light in lights:
        light.image = Assets.squishedTiles[4]
        virtual_screen.blit(pygame.transform.scale(light.image, (36, 8)), light.rect)

    virtual_screen.blit(ValveDoor1.image, ValveDoor1.rect)
    virtual_screen.blit(ValveDoor2.image, ValveDoor2.rect)
    virtual_screen.blit(ValveDoor3.image, ValveDoor3.rect)
    virtual_screen.blit(exitDoor.image, exitDoor.rect)
    virtual_screen.blit(window, (-42, 22))
    virtual_screen.blit(window, (157, 22))
    virtual_screen.blit(window, (358, 22))
    virtual_screen.blit(window, (558, 22))
    Player.animatePlayer(virtual_screen, player_pos)

    # if not Objects.getPinkPower():
    #     if power and level == 3:
    #         # the lights are done using an array like this because apply_lighting() only works properly if all the lights in the room are in 1 array. Does not work properly if called multiple times
    #         # remove upper and lower lights
    #         while len(lightsNew) > 3:
    #             lightsNew.pop()

    #         # apply lighting
    #         apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    #         apply_falloff(falloffPartial, virtual_screen, ambientLightPos)
    #         apply_falloff(falloffPartial, virtual_screen, (lightsNew[1].x, lightsNew[1].y))  
    #         apply_falloff(falloffPartial, virtual_screen, (lightsNew[2].x, lightsNew[2].y))  
    #         apply_falloff(falloffPartial, virtual_screen, (lightsNew[3].x, lightsNew[3].y)) 
            
    # else:
    #     if len(lightsNew) != 5: # reset lights array if the right amount of lights is not in it
    #         while len(lightsNew) > 3:
    #                 lightsNew.pop()

    #     # apply lighting
    #     apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    #     apply_falloff(falloff, virtual_screen, ambientLightPos)
    #     apply_falloff(falloff, virtual_screen, (lightsNew[1].x, lightsNew[1].y))  
    #     apply_falloff(falloff, virtual_screen, (lightsNew[2].x, lightsNew[2].y)) 
    #     apply_falloff(falloff, virtual_screen, (lightsNew[3].x, lightsNew[3].y)) 
    #     apply_falloff(falloff, virtual_screen, (lightsNew[4].x, lightsNew[4].y)) 

    virtual_screen.blit(dark_overlay, (0, 0))

    virtual_view = virtual_screen.subsurface((max(min(player_pos.x - 208, virtual_screen.get_width()/2), 0),0,virtual_view_res[0],virtual_view_res[1]))

    Assets.scaled_draw(virtual_view_res, virtual_view, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
