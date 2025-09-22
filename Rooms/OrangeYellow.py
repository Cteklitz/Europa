import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items

virtual_res = (124,90)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

orangeyellowclosed = pygame.image.load("Assets/orangeyellowclosed.png")
orangeyellowopen = pygame.image.load("Assets/orangeyellowopen.png")
orangeyellowopenpetri = pygame.image.load("Assets/orangeyellowopenpetri.png")

open = False
yellowFound = False
exit = False

orangeRect = pygame.Rect(18,23,62,27)
petriRect = pygame.Rect(45,37,23,10)

def inBounds(x, y):
    global exit, open
    if exit:
        open = False
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, open, yellowFound
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
                    if not open and orangeRect.collidepoint(mouse_pos):
                        Sounds.book.play()
                        open = True
                    elif open and not yellowFound and petriRect.collidepoint(mouse_pos):
                        # add yellow petri to inventory
                        if (Player.addItem(Items.yellowPetri)):
                            Sounds.glass1.play()
                            yellowFound = True

    if not open:
        virtual_screen.blit(orangeyellowclosed, (0,0))
    else:
        if yellowFound:
            virtual_screen.blit(orangeyellowopen, (0,0))
        else:
            virtual_screen.blit(orangeyellowopenpetri, (0,0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale