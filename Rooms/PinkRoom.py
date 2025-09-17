import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds

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

valve = Objects.Valve(96, 112, divertWater)

def inBounds(x, y):
    level, power = Objects.getPipeDungeonInfo()
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
    elif not outline.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "MainRoom":
        player_pos = pygame.Vector2(pinkDoor.x - 5, pinkDoor.y + pinkDoor.rect.height/2)
    if cameFrom == "PinkUpperWing":
        player_pos = pygame.Vector2(northDoor.x + northDoor.rect.width/2, northDoor.y + northDoor.rect.height + 5)
    if cameFrom == "PinkLowerWing":
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
                Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (100, 0, 100))
                virtual_screen.blit(shadow, shadowRect)
                Done = True
            virtual_screen.blit(light.image, light.rect)
    else:
        for light in lights:
            light.update()
            if not Done:
                upperWingLight.image = Assets.tiles[1]
                lowerWingLight.image = Assets.tiles[1]
                Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (100, 0, 100))
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

    if player_pos.y < 124:
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)
        virtual_screen.blit(valve.image, valve.rect)
    else:
        virtual_screen.blit(valve.image, valve.rect)
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    virtual_screen.blit(dark_overlay, (0, 0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, screen.get_width()/virtual_screen.get_width(), screen.get_height()/virtual_screen.get_height()