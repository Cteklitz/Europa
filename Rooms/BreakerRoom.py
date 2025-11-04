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
    Objects.Light(176, 48, 2),
    Objects.Light(176, 176, 2),
    Objects.Light(48, 48, 2),
    Objects.Light(48, 176, 2)
]

northDoor = Objects.Door(112, 16, Assets.lockedDoorNorth)
westDoor = Objects.Door(16, 112, Assets.grayDoorWest)
toolboxGround = Assets.toolboxGround

breakerBox = Assets.breakerBox
breakerRect = pygame.Rect(150, 17, 32, 32)

toolbox = False
toolboxRect = pygame.Rect(190, 115, 19, 28)
toolboxInteractRect = pygame.Rect(185, 110, 29, 38)

# prevents player from walking into walls/objects
def inBounds(x, y):
    global toolbox
    level, power = Objects.getPipeDungeonInfo()
    if toolbox:
        toolbox = False
        return 2
    if westDoor.rect.collidepoint((x,y)):
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 0
    elif northDoor.rect.collidepoint((x,y)):
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 1
    elif not outline.contains(Point(x,y)):
        return False
    elif toolboxRect.collidepoint((x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.BlueRoom":
        player_pos = pygame.Vector2(westDoor.x + 37, westDoor.y + westDoor.rect.height/2)
    if cameFrom == "Rooms.PuddleRoom":
        player_pos = pygame.Vector2(northDoor.x + northDoor.rect.width/2, northDoor.y + northDoor.rect.height + 5)

def Room(screen, screen_res, events):
    global toolbox
    level, power = Objects.getPipeDungeonInfo()
    
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if toolboxInteractRect.collidepoint(player_pos):
                    toolbox = True

             
    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "gray", 1, True)
    outer = Assets.draw_polygon(virtual_screen, (240, 240), 4, 224, "black")
    inner = Assets.draw_polygon(virtual_screen, (208, 208), 4, 160, "black")
    for i in range(4):
        pygame.draw.line(virtual_screen, "black", outer[i], inner[i], 1)

    Done = False

    for light in lights:
        light.update()
        if not Done:
            Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (0, 162, 232))
            Done = True
        virtual_screen.blit(light.image, light.rect)

    virtual_screen.blit(northDoor.image, northDoor.rect)
    virtual_screen.blit(westDoor.image, westDoor.rect)
    virtual_screen.blit(breakerBox, breakerRect)
    virtual_screen.blit(toolboxGround, (190, 115))

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
