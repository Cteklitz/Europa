import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random
import Player
import Items

virtual_res = (203, 145)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

background = pygame.image.load("Assets/Safe.png")
background2 = pygame.image.load("Assets/OpenSafe.png")

exit = False
solved = False
collected = False
played = False

numbers = [
    Objects.Code(43,25),
    Objects.Code(86,25),
    Objects.Code(129,25)
]

letterRect = Polygon([(39,49),(61,31),(101,83),(75,102)])

def inBounds(x, y):
    global exit, solved, played
    if exit:
        solved = False
        exit = False
        played = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, solved, collected, played
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    _, lowerWingPower = Objects.getPinkWingInfo()
    lit = lowerWingPower and level == 1 and power

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                if not solved:
                    for number in numbers:
                        if number.rect.collidepoint(mouse_pos):
                            Sounds.combo.play()
                            if number.state == 9:
                                number.state = 0
                            else:
                                number.state += 1
                            if numbers[0].state == 2 and numbers[1].state == 7 and numbers[2].state == 5:
                                if not played:
                                    played = True
                                    Sounds.letter.play()
                                solved = True
                                for number in numbers:
                                    number.state = 0
                else:
                    if letterRect.contains(Point(mouse_pos)) and not collected:
                        if (Player.addItem(Items.letterTile)):
                            Sounds.letter.play()
                            collected = True
                    
    virtual_screen.fill((195, 195, 195))
    dark_overlay.fill((0, 0, 0, 150))

    if not solved:
        virtual_screen.blit(background, (0,0))
        for number in numbers:
            virtual_screen.blit(Assets.numberTiles[number.state], number.rect)
    else:
        virtual_screen.blit(background2, (0,0))
        if collected:
            pygame.draw.rect(virtual_screen, "black", (32,29,71,78))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale