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

upperWingLight = Objects.Light(48, 48, 1)
lowerWingLight = Objects.Light(48, 176, 1)

lights = [
    Objects.Light(176, 48, 1),
    Objects.Light(176, 176, 1)
]

# New Lighting
pinkLightRadius = 25
pinkLightStrength = 100
#pinkLightColor = (245, 118, 238)
pinkLightColor = (255, 20, 243)
ambientLightPos = (256/2, 256/2)
lightsNew = [LightSource(ambientLightPos[0], ambientLightPos[1], radius=60, strength = 200),
             LightSource(lights[0].x + 16, lights[0].y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor),
             LightSource(lights[1].x + 16, lights[1].y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 50)]
falloffPartial = [LightFalloff(virtual_screen.get_size(), darkness = 75)]

upperWingPinkLight = LightSource(upperWingLight.x + 16, upperWingLight.y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor)
lowerWingPinkLight = LightSource(lowerWingLight.x + 16, lowerWingLight.y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor)


pinkDoor = Objects.Door(208, 112, Assets.pinkDoorEast)
northDoor = Objects.Door(112, 16, Assets.grayDoorNorth)
southDoor = Objects.Door(112, 208, Assets.grayDoorSouth)

upperWingPower = False
lowerWingPower = False

def divertWater():
    global upperWingPower, lowerWingPower
    level, power = Objects.getPipeDungeonInfo()
    if level == 1 and power:
        if upperWingPower:
            upperWingPower = False
            lowerWingPower = True
        else:
            upperWingPower = True
            lowerWingPower = False

valve = Objects.TopDownValve(96, 112, divertWater)

def inBounds(x, y):
    level, power = Objects.getPipeDungeonInfo()
    valveRect = pygame.Rect(93,113,34,20)
    if pinkDoor.rect.collidepoint((x,y)):
        if level == 1 and power or Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 0
    elif southDoor.rect.collidepoint((x,y)):
        if level == 1 and power and not lowerWingPower and not Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 1
    elif northDoor.rect.collidepoint((x,y)):
        if level == 1 and power and not upperWingPower and not Objects.getPinkPower():
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 2
    elif valveRect.collidepoint((x,y)):
        return False
    elif not outline.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.MainRoom":
        player_pos = pygame.Vector2(pinkDoor.x - 5, pinkDoor.y + pinkDoor.rect.height/2)
    if cameFrom == "Rooms.PinkUpperWing":
        player_pos = pygame.Vector2(northDoor.x + northDoor.rect.width/2, northDoor.y + northDoor.rect.height + 5)
    if cameFrom == "Rooms.PinkLowerWing":
        player_pos = pygame.Vector2(southDoor.x + southDoor.rect.width/2, southDoor.y - 5)

def Room(screen, screen_res, events):
    global upperWingPower, lowerWingPower
    level, power = Objects.getPipeDungeonInfo()
    if not upperWingPower and not lowerWingPower and level == 1 and power:
        lowerWingPower = True

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                valve.check_collision(player_pos)

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "gray", 1, True)
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "black")
    inner = Assets.draw_polygon(virtual_screen, (208, 208), 4, 160, "black")
    for i in range(4):
        pygame.draw.line(virtual_screen, "black", outer[i], inner[i], 1)

    Done = False

    if not Objects.getPinkPower():
        for light in lights:
            lit = light.update()
            if not Done and lit:
                if upperWingPower:
                    upperWingLight.image = Assets.tiles[1]
                    lowerWingLight.image = Assets.dimTiles[1]
                    shadowRect = pygame.Rect(0,144,112,112)
                    shadow = virtual_screen.subsurface(shadowRect).copy()
                elif lowerWingPower:
                    lowerWingLight.image = Assets.tiles[1]
                    upperWingLight.image = Assets.dimTiles[1]
                    shadowRect = pygame.Rect(0,0,112,112)
                    shadow = virtual_screen.subsurface(shadowRect).copy()
                Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (1, 0, 1))
                virtual_screen.blit(shadow, shadowRect)
                Done = True
            virtual_screen.blit(light.image, light.rect)
    else:
        for light in lights:
            light.update()
            if not Done:
                upperWingLight.image = Assets.tiles[1]
                lowerWingLight.image = Assets.tiles[1]
                Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (1, 0, 1))
                Done = True
            virtual_screen.blit(light.image, light.rect)

    virtual_screen.blit(Assets.pipes[11], (112,112))
    virtual_screen.blit(Assets.pipes[10], (144,112))
    virtual_screen.blit(Assets.pipes[10], (176,112))
    virtual_screen.blit(Assets.pipes[7], (112,48))
    virtual_screen.blit(Assets.pipes[7], (112,80))
    virtual_screen.blit(Assets.pipes[7], (112,144)) 
    virtual_screen.blit(Assets.pipes[7], (112,176))

    if (not power or level != 1) and not Objects.getPinkPower():
        lowerWingLight.image = Assets.dimTiles[1]
        upperWingLight.image = Assets.dimTiles[1]

    virtual_screen.blit(upperWingLight.image, upperWingLight.rect)
    virtual_screen.blit(lowerWingLight.image, lowerWingLight.rect)

    virtual_screen.blit(pinkDoor.image, pinkDoor.rect)
    virtual_screen.blit(northDoor.image, northDoor.rect)
    virtual_screen.blit(southDoor.image, southDoor.rect)

    valve.update()

    if player_pos.y < 132:
        Player.animatePlayer(virtual_screen, player_pos, 32, 32, "top-down")
        virtual_screen.blit(valve.image, valve.rect)
    else:
        virtual_screen.blit(valve.image, valve.rect)
        Player.animatePlayer(virtual_screen, player_pos, 32, 32, "top-down")

    if not Objects.getPinkPower():
        if power and level == 1:
            # the lights are done using an array like this because apply_lighting() only works properly if all the lights in the room are in 1 array. Does not work propely if called multiple times
            # remove upper and lower lights
            while len(lightsNew) > 3:
                lightsNew.pop()

            if upperWingPower: # add upper light to lights array             
                lightsNew.append(upperWingPinkLight)
            if lowerWingPower: # add lower light to lights array             
                lightsNew.append(lowerWingPinkLight)

            # apply lighting
            apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
            apply_falloff(falloffPartial, virtual_screen, ambientLightPos)
            apply_falloff(falloffPartial, virtual_screen, (lightsNew[1].x, lightsNew[1].y))  
            apply_falloff(falloffPartial, virtual_screen, (lightsNew[2].x, lightsNew[2].y))  
            apply_falloff(falloffPartial, virtual_screen, (lightsNew[3].x, lightsNew[3].y)) 
            
    else:
        if len(lightsNew) != 5: # reset lights array if the right amount of lights is not in it
            while len(lightsNew) > 3:
                    lightsNew.pop()
        if len(lightsNew) == 3:
            lightsNew.append(upperWingPinkLight)
            lightsNew.append(lowerWingPinkLight)

        # apply lighting
        apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
        apply_falloff(falloff, virtual_screen, ambientLightPos)
        apply_falloff(falloff, virtual_screen, (lightsNew[1].x, lightsNew[1].y))  
        apply_falloff(falloff, virtual_screen, (lightsNew[2].x, lightsNew[2].y)) 
        apply_falloff(falloff, virtual_screen, (lightsNew[3].x, lightsNew[3].y)) 
        apply_falloff(falloff, virtual_screen, (lightsNew[4].x, lightsNew[4].y)) 

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
