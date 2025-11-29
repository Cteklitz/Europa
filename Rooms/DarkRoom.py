import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player

virtual_res = (324, 219)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(239, 180)

bounds = Polygon([(39, 102), (294, 102), (305, 174), (25, 174)])

# south exit
exitRect = pygame.Rect(247, 188, 58, 31)
exitWalk = pygame.Rect(247, 174, 58, 45)

# north exit
exitRect2 = pygame.Rect(192, 48, 59, 63)

falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

background = pygame.image.load("Assets/DarkRoom.png")
shadow = pygame.image.load("Assets/Shadow.png")
tooDarkScale = pygame.transform.scale(Assets.tooDark, (Assets.tooDark.get_width()/1.25,Assets.tooDark.get_height()/1.25))
tooDark = Objects.briefText(virtual_screen, tooDarkScale, 15, 180, 3)

animation = []
for i in range(1, 16):
    animation.append(pygame.image.load(f"Assets/screenshot{i}.png"))

played = False

def inBounds(x, y):
    shadowBound = Polygon([(59,0),(0,0),(0,219),(259,219)])
    if exitRect.collidepoint((x,y)):
        tooDark.activated_time = -1
        return 0
    if exitRect2.collidepoint((x,y)):
        tooDark.activated_time = -1
        return 1
    elif exitWalk.collidepoint(x,y):
        return True
    elif not bounds.contains(Point(x,y)):
        return False
    elif shadowBound.contains(Point(x,y)):
        tooDark.activated_time = pygame.time.get_ticks()
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos, played
    if not played:
        Sounds.whatAwaits.play(-1)
        played = True
    if cameFrom == "Rooms.YellowRoom":
        player_pos = pygame.Vector2(exitWalk.centerx + 2, exitWalk.centery - 20)
    if cameFrom == "Rooms.MscopeTable":
        pass

def Room(screen, screen_res, events):
    global trianglePuzzle1, trianglePuzzle2, whiteboard, beaker, table, tableboundRect

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = (upperWingPower and level == 1 and power) or Objects.getPinkPower()

    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

    virtual_screen.blit(background, (0,0))
    dark_overlay.fill((0, 0, 0, 200))

    Player.animatePlayer(virtual_screen, player_pos)

    virtual_screen.blit(shadow, (10,0))

    virtual_screen.blit(dark_overlay, (0, 0))

    tooDark.update()

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3.5, 3.5  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
