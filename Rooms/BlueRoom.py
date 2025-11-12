import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player

virtual_res = (256, 256)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

bounds = Assets.draw_polygon(virtual_screen, (208, 208), 4, 160, "gray")
outline = Polygon(bounds)

lights = [
    Objects.Light(176, 144, 2),
    Objects.Light(48, 48, 2),
    Objects.Light(48, 176, 2),
    Objects.Light(176, 80, 1)
]

ambientLightPos = (256/2, 256/2)
lightsNew = [LightSource(ambientLightPos[0], ambientLightPos[1], radius=40, strength = 150)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 200)]
pinkLight = [LightSource(176 + 16, 80 + 16, radius=20, strength = 150, color=(150,0,100))]

blueDoor = Objects.Door(16, 112, Assets.blueDoorWest)
lockedDoor = Objects.Door(208, 112, Assets.lockedDoorEast)

open = False

def inBounds(x, y):
    global open
    level, power = Objects.getPipeDungeonInfo()
    if blueDoor.rect.collidepoint((x,y)):
        if (level == 2 and power) or Objects.getBluePower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 0
    if lockedDoor.rect.collidepoint((x,y)) and open:
        return 1
    elif not outline.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.MainRoom":
        player_pos = pygame.Vector2(blueDoor.x + 37, blueDoor.y + blueDoor.rect.height/2)

def Room(screen, screen_res, events):
    global open
    
    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "gray", 1, True)
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "black")
    inner = Assets.draw_polygon(virtual_screen, (208, 208), 4, 160, "black")
    for i in range(4):
        pygame.draw.line(virtual_screen, "black", outer[i], inner[i], 1)

    Done = False
    pink = False
    blue = False

    for light in lights:
        lit = light.update()
        if lit and light.type == 1:
            #Assets.punch_light_hole(virtual_screen, dark_overlay, (192,96), 50, (0, 0, 0))
            pink = True
        if not Done and lit and light.type == 2:
            Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (0, 0, 0))
            Done = True
            blue = True
        virtual_screen.blit(light.image, light.rect)

    for x in range(48, 208, 32):
        virtual_screen.blit(Assets.pipes[10], (x,112))

    virtual_screen.blit(blueDoor.image, blueDoor.rect)

    # TODO: Door always open for testing. Change before final version
    open = True
    lockedDoor.image = Assets.grayDoorEast
    # if pink and blue:
    #     open = True
    #     lockedDoor.image = Assets.grayDoorEast
    # else:
    #     open = False
    #     lockedDoor.image = Assets.lockedDoorEast
    
    virtual_screen.blit(lockedDoor.image, lockedDoor.rect)

    Player.animatePlayer(virtual_screen, player_pos, 32, 32, "top-down")

    if blue: # apply standard lighting if blue power is on
        apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(20, 20, 20), ambient_strength=5)
        apply_falloff(falloff, virtual_screen, ambientLightPos)
    elif pink: # apply special pink lighting if only pink is on
        apply_lighting(virtual_screen, pinkLight, darkness=10, ambient_color=(20, 20, 20), ambient_strength=5)
        apply_falloff(falloff, virtual_screen, (pinkLight[0].x,pinkLight[0].y))


    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
