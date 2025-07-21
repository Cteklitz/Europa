import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random

virtual_res = (213, 134)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

background = pygame.image.load("Assets/mscopetablezoom.png")
opendrawer = pygame.image.load("Assets/opendrawer.png")
redpetri = pygame.image.load("Assets/redpetri.png")
redRect = pygame.Rect(82, 57, 11, 6)
yellowpetri = pygame.image.load("Assets/yellowpetri.png") 
yellowRect = pygame.Rect(103, 52, 11, 6)
bluepetri = pygame.image.load("Assets/bluepetri.png") 
blueRect = pygame.Rect(98, 64, 11, 6)

Cover = pygame.Surface((11, 6))
Cover.fill((127,127,127))
msRect = pygame.Rect(54,44,11,6)

MSRect = pygame.Rect(40,24,32,43)

exit = False
luckyNumber = random.randint(1,12)
redFound = False
selected = "None"
microscope = False

drawerTimer = Objects.timer(0.5, False)

class Drawer:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 36, 12)
        self.state = "closed"

drawers = []
for y in range(3):
    for x in range(4):
        drawers.append(Drawer(33+(37*x), 90+(13*y)))

luckyRect = pygame.Rect(drawers[luckyNumber-1].rect.x+14, drawers[luckyNumber-1].rect.y, 11,5)

def inBounds(x, y):
    global exit, microscope
    if exit:
        exit = False
        return 0
    elif microscope:
        microscope = False
        return 1
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, redFound, visible, selected, microscope
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = upperWingPower and level == 1 and power

    _, yellowFound, blueFound = Objects.getColors()

    visible = False

    if drawers[luckyNumber-1].state == "open":
        above = luckyNumber - 5
        if above >= 0:
            if drawers[above].state == "closed":
                visible = True
        else:
            visible = True

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                if luckyRect.collidepoint(mouse_pos) and visible:
                    Sounds.glass1.play()
                    redFound = True
                elif redRect.collidepoint(mouse_pos) and redFound:
                    selected = "Red"
                elif yellowRect.collidepoint(mouse_pos) and yellowFound:
                    selected = "Yellow"
                elif blueRect.collidepoint(mouse_pos) and blueFound:
                    selected = "Blue"
                elif msRect.collidepoint(mouse_pos):
                    selected = "None"
                elif MSRect.collidepoint(mouse_pos) and selected != "None":
                    microscope = True
                for drawer in drawers:
                    if drawer.rect.collidepoint(mouse_pos):
                        if drawer.state == "closed":
                            Sounds.drawerclose.stop()
                            Sounds.draweropen.play()
                            drawer.state = "open"
                            drawer.rect.y += 4
                        else:
                            Sounds.draweropen.stop()
                            Sounds.drawerclose.play()
                            drawer.state = "closed"
                            drawer.rect.y -= 4
                        break
                    
    virtual_screen.fill((195, 195, 195))
    dark_overlay.fill((0, 0, 0, 150))

    Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    virtual_screen.blit(background, (0,0))

    count = 12
    for drawer in reversed(drawers):
        if drawer.state == "open":
            virtual_screen.blit(opendrawer, (drawer.rect.x, drawer.rect.y-4))
            if count == luckyNumber and not redFound and visible:
                virtual_screen.blit(redpetri, luckyRect, area=pygame.Rect(0, 0, 11, 5))
        count -= 1

    if not redFound or selected == "Red":
        virtual_screen.blit(Cover, redRect)
        if selected == "Red":
            virtual_screen.blit(redpetri, msRect)

    if not yellowFound or selected == "Yellow":
        virtual_screen.blit(Cover, yellowRect)
        if selected == "Yellow":
            virtual_screen.blit(yellowpetri, msRect)

    if not blueFound or selected == "Blue":
        virtual_screen.blit(Cover, blueRect)
        if selected == "Blue":
            virtual_screen.blit(bluepetri, msRect)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale