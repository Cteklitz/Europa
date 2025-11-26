import pygame
import Assets
import Objects
import Items
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player

virtual_res = (648,357)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_res2 = (400, 219)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay2 = pygame.Surface(virtual_screen2.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(239, 180)

fertilizer = pygame.image.load("Assets/Fertilizer.png")
fertilizer_pos = (20, 90)

rake = pygame.image.load("Assets/Rake.png")
rake_pos = (45, 75)

waterCan = pygame.image.load("Assets/WaterCan.png")
waterCan_pos = (15, 120)

bounds = Polygon([(32,224),(0,287),(227,280),(453,247),(453,224)])

lit = False
light_pos = (70, 50)
light_pos2 = (240, 50)
wall_lights = [
    LightSource(light_pos[0], light_pos[1], radius=60, strength = 220),
    LightSource(light_pos2[0], light_pos2[1], radius=60, strength = 220)
]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

# load assets
background = pygame.image.load("Assets/SubRoom.png")
exitRect = pygame.Rect(4, 175, 21, 115)

def inBounds(x, y):
    if exitRect.collidepoint((x,y)):
        return 0
    elif not bounds.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.YellowHallway":
        player_pos = pygame.Vector2(exitRect.centerx + 35, exitRect.centery + 25)

def Room(screen, screen_res, events):
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:
    
    virtual_screen.blit(background, (0,0))

    Player.animatePlayer(virtual_screen, player_pos)

    apply_lighting(virtual_screen, wall_lights, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    apply_falloff(falloff, virtual_screen, light_pos)

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3.5, 3.5  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
