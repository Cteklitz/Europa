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

lights = [
    Objects.Light(176, 144, 2),
    Objects.Light(48, 48, 2),
    Objects.Light(48, 176, 2),
    Objects.Light(176, 80, 1)
]

blueDoor = Objects.Door(16, 112, Assets.blueDoorWest)
lockedDoor = Objects.Door(208, 112, Assets.lockedDoorEast)

def inBounds(x, y):
    level, power = Objects.getPipeDungeonInfo()
    if blueDoor.rect.collidepoint((x,y)):
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 0
    elif not outline.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.MainRoom":
        player_pos = pygame.Vector2(blueDoor.x + 37, blueDoor.y + blueDoor.rect.height/2)

def Room(screen, screen_res, events):
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
            Assets.punch_light_hole(virtual_screen, dark_overlay, (192,96), 50, (100, 0, 100))
            pink = True
        if not Done and lit and light.type == 2:
            Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (0, 162, 232))
            Done = True
            blue = True
        virtual_screen.blit(light.image, light.rect)

    for x in range(48, 208, 32):
        virtual_screen.blit(Assets.pipes[10], (x,112))

    virtual_screen.blit(blueDoor.image, blueDoor.rect)

    if pink and blue:
        lockedDoor.image = Assets.grayDoorEast
    else:
        lockedDoor.image = Assets.lockedDoorEast
    
    virtual_screen.blit(lockedDoor.image, lockedDoor.rect)

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    virtual_screen.blit(dark_overlay, (0, 0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, screen.get_width()/virtual_screen.get_width(), screen.get_height()/virtual_screen.get_height()