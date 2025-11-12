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
    Objects.Light(176, 48, 2),
    Objects.Light(176, 176, 2),
    Objects.Light(48, 48, 2),
    Objects.Light(48, 176, 2)
]

ambientLightPos = (256/2, 256/2)
lightsNew = [LightSource(ambientLightPos[0], ambientLightPos[1], radius=40, strength = 150)]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 200)]

northDoor = Objects.Door(112, 16, Assets.lockedDoorNorth)
northDoorUnlocked = Objects.Door(112, 16, Assets.grayDoorNorth)
westDoor = Objects.Door(16, 112, Assets.grayDoorWest)
toolboxGround = Assets.toolboxGround

breakerBox = Assets.breakerBox
breakerRect = pygame.Rect(150, 17, 32, 32)
breakerInteractRect = pygame.Rect(150, 48, 32, 16)

puzzle = False

toolbox = False
toolboxRect = pygame.Rect(190, 115, 19, 28)
toolboxInteractRect = pygame.Rect(185, 110, 29, 38)

# prevents player from walking into walls/objects
def inBounds(x, y):
    global toolbox
    global puzzle
    global solved

    level, power = Objects.getPipeDungeonInfo()
    if toolbox:
        toolbox = False
        return 3
    if westDoor.rect.collidepoint((x,y)):
        return 0
    elif northDoor.rect.collidepoint((x,y)):
        if solved:
            if not Objects.getBluePower():
                Sounds.powerAmb.stop()
                Sounds.ominousAmb.play(-1)
            return 1
        else:
            return False
    elif puzzle:
        puzzle = False
        return 2
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
    global puzzle
    level, power = Objects.getPipeDungeonInfo()
    global solved
    solved = Objects.getBreakerSolved()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if breakerInteractRect.collidepoint(player_pos):
                    puzzle = True
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
            Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (0, 0, 0))
            Done = True
        virtual_screen.blit(light.image, light.rect)

    if solved:
        virtual_screen.blit(northDoorUnlocked.image, northDoor.rect)
    else:
        virtual_screen.blit(northDoor.image, northDoor.rect)
    virtual_screen.blit(westDoor.image, westDoor.rect)
    virtual_screen.blit(breakerBox, breakerRect)
    virtual_screen.blit(toolboxGround, (190, 115))

    for x in range(48, 112, 32):
        virtual_screen.blit(Assets.pipes[10], (x,112))

    virtual_screen.blit(Assets.pipes[14], (112,112))

    for y in range(48, 112, 32):
        virtual_screen.blit(Assets.pipes[12], (112,y))

    Player.animatePlayer(virtual_screen, player_pos, 32, 32, "top-down")

    apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(20, 20, 20), ambient_strength=5)
    apply_falloff(falloff, virtual_screen, ambientLightPos)

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
