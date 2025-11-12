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

virtual_res = (644, 260)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_view_res = (virtual_screen.get_width()/2, virtual_screen.get_height())

player_pos = pygame.Vector2(192, 128)

lights = [
    Objects.Light(48, 48, 3),
    Objects.Light(48, 176, 3),
    Objects.Light(208, 176, 3),
    Objects.Light(400, 48, 3),
    Objects.Light(400, 176, 3),
    Objects.Light(560, 48, 3),
    Objects.Light(560, 176, 3)
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

greenDoor = Objects.Door(208, 16, Assets.greenDoorNorth)
bathroomDoor = Objects.Door(16, 112, Assets.grayDoorWest)
bedroom1Door = Objects.Door(112, 208, Assets.grayDoorSouth)
bedroom2Door = Objects.Door(304, 208, Assets.grayDoorSouth)
bedroom3Door = Objects.Door(496, 208, Assets.grayDoorSouth)
greenhouseDoor = Objects.Door(592, 112, Assets.grayDoorEast)

upperWingPower = False
lowerWingPower = False

Sounds.radioFar.play(-1)
Sounds.radioFar.set_volume(0)
Sounds.radioClose.play(-1)
Sounds.radioClose.set_volume(0)

def inBounds(x, y):
    level, power = Objects.getPipeDungeonInfo()
    bounds = pygame.Rect(48,48,544,160)
    # Add greenpower statement
    if level == 3 and power:
        greenPowerOn = True
    else:
        greenPowerOn = False
    #greenPowerOn = True # FOR TESTING

    if greenDoor.rect.collidepoint((x,y)):
        Sounds.radioFar.set_volume(0)
        if level == 3 and power and not upperWingPower and not Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 0
    elif bathroomDoor.rect.collidepoint((x,y)):
        Sounds.radioFar.set_volume(0)
        if level == 3 and power or Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 1
    elif bedroom1Door.rect.collidepoint((x,y)):
        Sounds.radioFar.set_volume(0)
        if level == 3 and power and not lowerWingPower and not Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        Objects.setBedroomNumber(1)
        return 2
    elif bedroom2Door.rect.collidepoint((x,y)):
        if greenPowerOn:
            Sounds.radioClose.set_volume(1)
        Sounds.radioFar.set_volume(0)
        if level == 3 and power and not lowerWingPower and not Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        Objects.setBedroomNumber(2)
        return 2
    elif bedroom3Door.rect.collidepoint((x,y)):
        Sounds.radioFar.set_volume(0)
        if level == 3 and power and not lowerWingPower and not Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        Objects.setBedroomNumber(3)
        return 2
    elif greenhouseDoor.rect.collidepoint((x,y)):
        Sounds.radioFar.set_volume(0)
        if level == 3 and power and not lowerWingPower and not Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 3
    elif not bounds.collidepoint((x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos

    level, power = Objects.getPipeDungeonInfo()
    # Add greenpower statement
    if level == 3 and power:
        greenPowerOn = True
    else:
        greenPowerOn = False
    #greenPowerOn = True # FOR TESTING

    Sounds.radioClose.set_volume(0)
    if (greenPowerOn):
        Sounds.radioFar.set_volume(1)

    if cameFrom == "Rooms.Bathroom":
        player_pos = pygame.Vector2(bathroomDoor.x + 37, bathroomDoor.y + bathroomDoor.rect.height/2)
    elif cameFrom == "Rooms.MainRoom":       
        Sounds.radioClose.set_volume(0)
        player_pos = pygame.Vector2(greenDoor.x + greenDoor.rect.width/2, greenDoor.y + greenDoor.rect.height + 5)
    elif cameFrom == "Rooms.Bedroom":
        if Objects.getBedroomNumber() == 1:
            player_pos = pygame.Vector2(bedroom1Door.x + bedroom1Door.rect.width/2, bedroom1Door.y - 5)
        elif Objects.getBedroomNumber() == 2:          
            player_pos = pygame.Vector2(bedroom2Door.x + bedroom2Door.rect.width/2, bedroom2Door.y - 5)
        elif Objects.getBedroomNumber() == 3:
            player_pos = pygame.Vector2(bedroom3Door.x + bedroom3Door.rect.width/2, bedroom3Door.y - 5)
    elif cameFrom == "Rooms.Greenhouse":
        player_pos = pygame.Vector2(greenhouseDoor.x - 5, greenhouseDoor.y + greenhouseDoor.rect.height/2)   

def Room(screen, screen_res, events):
    global upperWingPower, lowerWingPower
    level, power = Objects.getPipeDungeonInfo()
    # Add greenpower statement
    if level == 3 and power:
        greenPowerOn = True
    else:
        greenPowerOn = False
    #greenPowerOn = True # FOR TESTING
    if not upperWingPower and not lowerWingPower and level == 3 and power:
        lowerWingPower = True

    # set radioFar volume based on distance to bedroom 2
    dist = math.sqrt((player_pos.x - bedroom2Door.x)**2 + (player_pos.y - bedroom2Door.y)**2)
    maxDist = math.sqrt((48 - bedroom2Door.x)**2 + (48 - bedroom2Door.y)**2)
    normDist = dist / maxDist # normalize dist
    vol = 1 - normDist + 0.2
    vol = vol**2 # apply expontial growth so vol scales smoothly
    Sounds.radioFar.set_volume(vol)

    if not greenPowerOn:
        Sounds.radioFar.set_volume(0)

    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    # outer rect
    outerRect = pygame.Rect(16,16,608,224)
    pygame.draw.rect(virtual_screen, "gray", outerRect)
    pygame.draw.rect(virtual_screen, "black", outerRect, 1)
    # inner rect
    innerRect = pygame.Rect(48,48,544,160)
    pygame.draw.rect(virtual_screen, "black", innerRect, 1)
    
    for i in (0, 1):
        for j in (0, 1):
            x1 = outerRect.left + i * outerRect.width
            y1 = outerRect.top + j * outerRect.height
            x2 = innerRect.left + i * innerRect.width
            y2 = innerRect.top + j * innerRect.height
            pygame.draw.line(virtual_screen, "black", (x1, y1), (x2, y2))

    Done = False

    if not Objects.getPinkPower():
        for light in lights:
            lit = light.update()
            if not Done and lit:
                if upperWingPower:
                    shadowRect = pygame.Rect(0,144,112,112)
                    shadow = virtual_screen.subsurface(shadowRect).copy()
                elif lowerWingPower:
                    shadowRect = pygame.Rect(0,0,112,112)
                    shadow = virtual_screen.subsurface(shadowRect).copy()
                Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (1, 0, 1))
                virtual_screen.blit(shadow, shadowRect)
                Done = True
            virtual_screen.blit(light.image, light.rect)
    else:
        for light in lights:
            light.update()
            if not Done:
                Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (1, 0, 1))
                Done = True
            virtual_screen.blit(light.image, light.rect)

    virtual_screen.blit(greenDoor.image, greenDoor.rect)
    virtual_screen.blit(bathroomDoor.image, bathroomDoor.rect)
    virtual_screen.blit(bedroom1Door.image, bedroom1Door.rect)
    virtual_screen.blit(bedroom2Door.image, bedroom2Door.rect)
    virtual_screen.blit(bedroom3Door.image, bedroom3Door.rect)
    virtual_screen.blit(greenhouseDoor.image, greenhouseDoor.rect)

    Player.animatePlayer(virtual_screen, player_pos, 32, 32, "top-down")

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
