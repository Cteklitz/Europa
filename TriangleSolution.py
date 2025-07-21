import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds

virtual_res = (750,500)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False

triangles = {}
for i in range(17):
    triangles[i+1] = pygame.image.load(f"Assets/Triangle{i+1}.png")

hint = pygame.image.load("Assets/hint.png")

gridPos = {
    1: (80,100),
    2: (150,98),
    3: (220,100),
    4: (290,98),
    5: (360,100),
    6: (430,98),
    7: (500,100),
    8: (80,224),
    9: (150,226),
    10: (220,224),
    11: (290,226),
    12: (360,224),
    13: (430,226),
    14: (500,224)
}

def inBounds(x, y):
    global exit, tooDark
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = upperWingPower and level == 1 and power

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
                    
    virtual_screen.fill((185, 122, 87))
    dark_overlay.fill((0, 0, 0, 150))

    for i in range(1,15):
        triangle, pos = triangles[i], gridPos[i]
        virtual_screen.blit(triangle, pos)

    pygame.draw.circle(virtual_screen, (255, 201, 14), (0,0), 35)
    pygame.draw.circle(virtual_screen, (255, 201, 14), (750,0), 35)
    pygame.draw.circle(virtual_screen, (255, 201, 14), (0,500), 35)
    pygame.draw.circle(virtual_screen, (255, 201, 14), (750,500), 35)

    virtual_screen.blit(hint, (190, 410))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale