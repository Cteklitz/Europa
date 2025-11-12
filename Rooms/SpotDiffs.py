import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items

virtual_res = (389,189)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

background = pygame.image.load("Assets/spotDiffs.png")
background2 = pygame.image.load("Assets/spotDiffs2.png")
background3 = pygame.image.load("Assets/spotDiffs3.png")

found = 0
collected = False
exit = False
chestOpen = False
played = False

mat = False
stem = False
corner = False
water = False
light = False
backgroundDiff = False

matRect = pygame.Rect(263,154,44,17)
stemRect = pygame.Rect(283,6,14,15)
cornerRect = pygame.Rect(309,83,12,12)
waterRect = pygame.Rect(202,87,23,11)
lightRect = pygame.Rect(353,16,23,20)
backgroundRect = pygame.Rect(194,0,195,81)

matRect2 = pygame.Rect(74,154,44,17)
stemRect2 = pygame.Rect(94,6,14,15)
cornerRect2 = pygame.Rect(121,83,12,12)
waterRect2 = pygame.Rect(11,87,23,11)
lightRect2 = pygame.Rect(164,16,23,20)
backgroundRect2 = pygame.Rect(0,0,197,81)

chairRect1 = pygame.Rect(14,21,76,57)
chairRect2 = pygame.Rect(110,21,76,57)
chairRect3 = pygame.Rect(205,21,76,57)
chairRect4 = pygame.Rect(298,21,76,57)

letterRect = pygame.Rect(168,119,42,28)

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, chestOpen, collected, mat, stem, corner, water, light, backgroundDiff, found, played
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
                    if matRect.collidepoint(mouse_pos) or matRect2.collidepoint(mouse_pos):
                        if not mat:
                            mat = True
                            found += 1
                    elif stemRect.collidepoint(mouse_pos) or stemRect2.collidepoint(mouse_pos):
                        if not stem:
                            stem = True
                            found += 1
                    elif cornerRect.collidepoint(mouse_pos) or cornerRect2.collidepoint(mouse_pos):
                        if not corner:
                            corner = True
                            found += 1
                    elif waterRect.collidepoint(mouse_pos) or waterRect2.collidepoint(mouse_pos):
                        if not water:
                            water = True
                            found += 1
                    elif lightRect.collidepoint(mouse_pos) or lightRect2.collidepoint(mouse_pos):
                        if not light:
                            light = True
                            found += 1
                    elif backgroundRect.collidepoint(mouse_pos) or backgroundRect2.collidepoint(mouse_pos):
                        if not chairRect1.collidepoint(mouse_pos) and not chairRect2.collidepoint(mouse_pos) and not chairRect3.collidepoint(mouse_pos) and not chairRect4.collidepoint(mouse_pos):
                            if not backgroundDiff:
                                backgroundDiff = True
                                found += 1
                    elif letterRect.collidepoint(mouse_pos) and chestOpen and not collected:
                        if (Player.addItem(Items.letterTile)):
                            Sounds.letter.play()
                            collected = True
                    if found == 6:
                        chestOpen = True
                        if not played:
                            played = True
                            Sounds.draweropen.play()

    virtual_screen.fill((195, 195, 195))

    Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    if not chestOpen:
        virtual_screen.blit(background, (0,0))
    else:
        if not Objects.getPinkPower():
            virtual_screen.blit(background2, (0,0))
        else:
            virtual_screen.blit(background3, (0,0))

    if mat:
        pygame.draw.rect(virtual_screen, "red", matRect, 3)
        pygame.draw.rect(virtual_screen, "red", matRect2, 3)
    if stem:
        pygame.draw.rect(virtual_screen, "red", stemRect, 3)
        pygame.draw.rect(virtual_screen, "red", stemRect2, 3)
    if corner:
        pygame.draw.rect(virtual_screen, "red", cornerRect, 3)
        pygame.draw.rect(virtual_screen, "red", cornerRect2, 3)
    if water:
        pygame.draw.rect(virtual_screen, "red", waterRect, 3)
        pygame.draw.rect(virtual_screen, "red", waterRect2, 3)
    if light:
        pygame.draw.rect(virtual_screen, "red", lightRect, 3)
        pygame.draw.rect(virtual_screen, "red", lightRect2, 3)
    if backgroundDiff:
        pygame.draw.rect(virtual_screen, "red", backgroundRect, 3)
        pygame.draw.rect(virtual_screen, "red", backgroundRect2, 3)
    if collected:
        pygame.draw.rect(virtual_screen, "black", letterRect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale