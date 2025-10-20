import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds

virtual_res = (416, 256)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

bounds = Polygon([(48,48), (368,48), (368,208), (48,208)])

lights = [
    Objects.Light(336, 80, 2),
    Objects.Light(336, 144, 2),
    Objects.Light(48, 48, 2),
    Objects.Light(48, 176, 2)
]

southDoor = Objects.Door((virtual_screen.get_width()/2) - 16, 208, Assets.grayDoorSouth)
westDoor = Objects.Door(16, 112, Assets.grayDoorWest)
eastDoor = Objects.Door(368, 112, Assets.grayDoorEast)
topRightWall = pygame.Rect(275, 48, 125, 31)
bottomRightWall = pygame.Rect(276, 176, 124, 32)

def inBounds(x, y):
    level, power = Objects.getPipeDungeonInfo()
    if southDoor.rect.collidepoint((x,y)):
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 0
    elif westDoor.rect.collidepoint((x,y)):
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 1
    elif eastDoor.rect.collidepoint((x,y)):
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 2
    elif not bounds.contains(Point(x,y)) or topRightWall.collidepoint((x,y)) or bottomRightWall.collidepoint((x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.BlueRoom":
        player_pos = pygame.Vector2(southDoor.x + 16, southDoor.y + 5)

def Room(screen, screen_res, events):
    level, power = Objects.getPipeDungeonInfo()
    
    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:
             
    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    outerRect = pygame.Rect((16,16,384,224))
    innerRect = pygame.Rect((48,48,320,160))

    # outer walls
    pygame.draw.rect(virtual_screen, "gray", outerRect)
    pygame.draw.rect(virtual_screen, "black", outerRect, 1)
    pygame.draw.rect(virtual_screen, "black", innerRect, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.topleft, innerRect.topleft, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.topright, innerRect.topright, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.bottomleft, innerRect.bottomleft, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.bottomright, innerRect.bottomright, 1)

    # hallway wall on bottom right
    pygame.draw.rect(virtual_screen, (105, 105, 105), (275, 176, 200, 200))
    pygame.draw.rect(virtual_screen, "black", (275, 176, 200, 200), 1)
    pygame.draw.line(virtual_screen, (105, 105, 105), (275,240), (275,256))
    pygame.draw.line(virtual_screen, (105, 105, 105), (400,176), (416,176))
    pygame.draw.rect(virtual_screen, "gray", bottomRightWall)
    pygame.draw.rect(virtual_screen, "black", bottomRightWall, 1)
    pygame.draw.line(virtual_screen, "gray", (398,176),(368,176), 2)
    pygame.draw.line(virtual_screen, "black", (399,207),(367,176))

    # hallway wall on top right
    pygame.draw.rect(virtual_screen, (105, 105, 105), (275, -120, 200, 200))
    pygame.draw.rect(virtual_screen, "black", (275, -120, 200, 200), 1)
    pygame.draw.line(virtual_screen, (105, 105, 105), (275,0), (275,15))
    pygame.draw.line(virtual_screen, (105, 105, 105), (400,79), (416,79))
    pygame.draw.rect(virtual_screen, "gray", topRightWall)
    pygame.draw.rect(virtual_screen, "black", topRightWall, 1)
    pygame.draw.line(virtual_screen, "gray", (398,78),(368,78), 2)
    pygame.draw.line(virtual_screen, "black", (399,48),(367,78))

    Done = False

    for light in lights:
        light.update()
        if not Done:
            #Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (0, 162, 232))
            Done = True
        virtual_screen.blit(light.image, light.rect)

    virtual_screen.blit(southDoor.image, southDoor.rect)
    virtual_screen.blit(westDoor.image, westDoor.rect)
    virtual_screen.blit(eastDoor.image, eastDoor.rect)

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    #virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
