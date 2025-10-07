import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Items

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

pinkKeycard = Objects.groundItem(150, 150, Items.pinkKeycard)
bandage = Objects.groundItem(300, 265, Items.bandage)

Sounds.ominousAmb.play(-1)

def inBounds(x, y):
    ctrlRmRect = pygame.Rect(220, 252, 36, 4)
    ctrlRmWallRect = pygame.Rect(208, 224, 63, 28)

    if ctrlRmRect.collidepoint((x,y)):
        pygame.mixer.music.load("Audio/electricbuzz.wav")
        pygame.mixer.music.play(-1)
        return 0
    elif pinkDoor.rect.collidepoint((x,y)):
        level, power = Objects.getPipeDungeonInfo()
        if power and level == 1 or Objects.getPinkPower():
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        return 1
    elif blueDoor.rect.collidepoint((x,y)):
        level, power = Objects.getPipeDungeonInfo()
        if power and level == 2:
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        return 2
    elif ctrlRmWallRect.collidepoint((x,y)):
        return False
    elif not octagon.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    ctrlRmRect = pygame.Rect(220, 252, 36, 4)
    if cameFrom == "Rooms.ControlRoom":
        player_pos = pygame.Vector2(ctrlRmRect.x + ctrlRmRect.width/2, ctrlRmRect.y + ctrlRmRect.height+5)
    if cameFrom == "Rooms.PinkRoom":
        player_pos = pygame.Vector2(pinkDoor.x + pinkDoor.rect.width+5, pinkDoor.y + pinkDoor.rect.height/2)
    if cameFrom == "Rooms.BlueRoom":
        player_pos = pygame.Vector2(blueDoor.x - 5, blueDoor.y + blueDoor.rect.height/2)
                                    
def Room(screen, screen_res, events):
    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    octagon1 = Assets.draw_polygon(virtual_screen, (336,470), 8, 192, "gray", 1, True)
    octagon1 = Assets.draw_polygon(virtual_screen, (336,470), 8, 192, "black")
    octagon2 = Assets.draw_polygon(virtual_screen, (320,430), 8, 160, "black")

    for i in range(8):
        pygame.draw.line(virtual_screen, "black", octagon1[i], octagon2[i], 1)

    # draw ground items
    Objects.groundItem.draw(pinkKeycard, virtual_screen)
    Objects.groundItem.draw(bandage, virtual_screen)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                pinkKeycard.check_collision(player_pos)
                bandage.check_collision(player_pos)

    lastType = 0

    for light in lights:
        if light.type != lastType:
            Done = False
        else:
            Done = True
        lastType = light.type
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

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
