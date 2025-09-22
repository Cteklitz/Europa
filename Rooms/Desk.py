import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items

virtual_res = (2000,1254)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

desk = pygame.image.load("Assets/DeskZoom.png")

blueFound = False
exit = False

petriRect = pygame.Rect(1241,505,460,233)

def inBounds(x, y):
    global exit, tooDark
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, blueFound
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                    if not blueFound and petriRect.collidepoint(mouse_pos):
                        # add blue petri to inventory
                        if (Player.addItem(Items.bluePetri)):
                            Sounds.glass1.play()
                            blueFound = True

    virtual_screen.blit(desk, (0,0))

    if blueFound:
        pygame.draw.rect(virtual_screen, (136,0,21), petriRect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale