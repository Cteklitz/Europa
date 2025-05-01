import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon

virtual_res = (480, 480)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(240, 340)

bounds = Assets.draw_polygon(virtual_screen, (320,430), 8, 160, "gray")
octagon = Polygon(bounds)

lights = [
    Objects.Light(47, 192, 1),
    Objects.Light(47, 256, 1),
    Objects.Light(401, 192, 2),
    Objects.Light(401, 256, 2),
    Objects.Light(192, 398, 3),
    Objects.Light(256, 398, 3),
    Objects.Light(192, 44, 4),
    Objects.Light(256, 44, 4)
]

pinkDoor = Objects.Door(15, 224, Assets.pinkDoorWest)
blueDoor = Objects.Door(433, 224, Assets.blueDoorEast)
greenDoor = Objects.Door(224, 430, Assets.greenDoorSouth)
orangeDoor = Objects.Door(224, 12, Assets.orangeDoorNorth)

def inBounds(x, y):
    ctrlRmRect = pygame.Rect(220, 252, 36, 4)
    ctrlRmWallRect = pygame.Rect(208, 224, 63, 28)

    if ctrlRmRect.collidepoint((x,y)):
        return 0
    elif pinkDoor.rect.collidepoint((x,y)):
        return 1
    elif ctrlRmWallRect.collidepoint((x,y)):
        return False
    elif not octagon.contains(Point(x,y)):
        return False
    return True

def Room(screen, screen_res, events):
    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    octagon1 = Assets.draw_polygon(virtual_screen, (336,470), 8, 192, "gray", 1, True)
    octagon1 = Assets.draw_polygon(virtual_screen, (336,470), 8, 192, "black")
    octagon2 = Assets.draw_polygon(virtual_screen, (320,430), 8, 160, "black")
    for i in range(8):
        pygame.draw.line(virtual_screen, "black", octagon1[i], octagon2[i], 1)

    Done = False

    for light in lights:
        lit = light.update()
        if lit:
            if light.type == 1:
                x = 15 + 16
                y = 224 + 16
            elif light.type == 2:
                x = 433 + 16
                y = 224 + 16
            elif light.type == 3:
                x = 224 + 16
                y = 430 + 16
            elif light.type == 4:
                x = 224 + 16
                y = 12 + 16
            if not Done:
                Assets.punch_light_hole(virtual_screen, dark_overlay, (x, y), 100, light.color)
                Done = True
            Assets.punch_light_hole(virtual_screen, dark_overlay, (light.x + 16, light.y + 16), 23, light.color)
        virtual_screen.blit(light.image, light.rect)

    Assets.punch_light_hole(virtual_screen, dark_overlay, (240,240), 23, (239,228,176))

    for y in range(44, 236, 32):
        virtual_screen.blit(Assets.pipes[7], (224, y))

    for y in range(238, 406, 32):
        virtual_screen.blit(Assets.pipes[7], (224, y))

    for x in range(47, 241, 32):
        virtual_screen.blit(Assets.pipes[10], (x, 224))

    for x in range(241, 431, 32):
        virtual_screen.blit(Assets.pipes[10], (x, 224))

    virtual_screen.blit(pinkDoor.image, pinkDoor.rect)
    virtual_screen.blit(blueDoor.image, blueDoor.rect)
    virtual_screen.blit(greenDoor.image, greenDoor.rect)
    virtual_screen.blit(orangeDoor.image, orangeDoor.rect)

    if player_pos.y < 240:
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)
        virtual_screen.blit(Assets.ctrlRoomDoor, (220, 224))
    else:
        virtual_screen.blit(Assets.ctrlRoomDoor, (220, 224))
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    virtual_screen.blit(dark_overlay, (0, 0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos