import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random
import Player
import Items

virtual_res = (275,216)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

lockedDoor = pygame.image.load("Assets/EYEDOOR.png")
openDoor = pygame.image.load("Assets/EYEDOOROPEN.png")

openSound = pygame.mixer.Sound("Audio/opensesame.wav")

exit = False
enter = False
solved = False
active = False
cutscene = False
played = False

timer1 = Objects.timer(4, False)
timer2 = Objects.timer(0.25, False)

doorY = 0
doorRect = pygame.Rect(0,0,openDoor.get_width(),openDoor.get_height())

letterCount = 0

letters = [
    Objects.Code(66, 50),
    Objects.Code(107, 50),
    Objects.Code(147, 50),
    Objects.Code(187, 50)
]

def inBounds(x, y):
    global exit, enter
    if exit:
        exit = False
        return 0
    elif enter:
        level, power = Objects.getPipeDungeonInfo()
        _, lowerWingPower = Objects.getPinkWingInfo()
        lit = lowerWingPower and level == 1 and power
        if not Objects.getPinkPower() and lit:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        enter = False
        return 1
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, solved, active, cutscene, doorY, enter, played, letterCount
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    _, lowerWingPower = Objects.getPinkWingInfo()
    lit = lowerWingPower and level == 1 and power

    #letterCount = Objects.getLetterCount()

    if letterCount == 4 and not solved:
        active = True

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and not cutscene:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = (mouse_x/xScale, mouse_y/yScale)
                for letter in letters:
                    if letter.rect.collidepoint(mouse_pos) and active: # increment letter value if all tiles are placed
                        Sounds.combo.play()
                        if letter.state == 25:
                            letter.state = 0
                        else:
                            letter.state += 1
                    elif letter.rect.collidepoint(mouse_pos) and not active: # place letter tile from inv if not all are placed
                        if (Player.checkItem(Items.letterTile)):
                            Player.removeItem(Items.letterTile)
                            Sounds.combo.play()
                            letterCount += 1              

                if letters[0].state == 12 and letters[1].state == 8 and letters[2].state == 13 and letters[3].state == 4:
                    solved  = True
                    active = False
                    timer1.setInitial()
                    timer2.setInitial()
                    if not played:
                        cutscene = True
                        played = True
                        openSound.play()

                if doorRect.collidepoint(mouse_pos) and solved and not cutscene:
                    enter = True
                    
    virtual_screen.fill((195, 195, 195))
    dark_overlay.fill((0, 0, 0, 150))

    if lit:
        Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    if cutscene:
        if timer2.Done():
            doorY += 1
        if timer1.Done():
            cutscene = False

    virtual_screen.blit(openDoor, (0,0))
    virtual_screen.blit(lockedDoor, (0,doorY))

    if letterCount != 0:
        for i in range(0,letterCount):
            if timer2.Done():
                letters[i].rect.y += 1
            virtual_screen.blit(Assets.letterTiles[letters[i].state], letters[i].rect)

    if not lit:
        virtual_screen.blit(dark_overlay, (0, 0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale