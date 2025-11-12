import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random

virtual_res = (1800,1200)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False

pieces = []
rects = []
for i in range(1, 25):
    pieces.append(pygame.image.load(f"Assets/tornPiece{i}.png"))
    rects.append(pieces[i-1].get_rect())
    rects[i-1].center = (random.randint(800,1000), random.randint(500,700))

dragging = False
dragRect = -1
offset_x = 0
offset_y = 0

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, dragging, offset_x, offset_y, dragRect
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                for i in range(0, len(rects)):
                    if rects[i].collidepoint(mouse_pos):
                        dragging = True
                        dragRect = i
                        offset_x = rects[i].centerx - mouse_pos[0]
                        offset_y = rects[i].centery - mouse_pos[1]
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
                dragRect = -1
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x / xScale, mouse_y / yScale)

                rects[dragRect].centerx = mouse_pos[0] + offset_x
                rects[dragRect].centery = mouse_pos[1] + offset_y
                    
    virtual_screen.fill((0,0,0))
    dark_overlay.fill((0, 0, 0, 150))

    for i in range(0, len(rects)):
        virtual_screen.blit(pieces[i], rects[i])

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale