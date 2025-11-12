import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player

virtual_res = (750,750)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

eye1 = pygame.image.load("Assets/MSEYE.png")
eye2 = pygame.image.load("Assets/MSEYE2.png")
eye3 = pygame.image.load("Assets/MSEYE3.png")
eye4 = pygame.image.load("Assets/MSEYE4.png")
eye5 = pygame.image.load("Assets/MSEYE5.png")

blue = pygame.image.load("Assets/msblue.png")
red = pygame.image.load("Assets/msred.png")
yellow = pygame.image.load("Assets/msyellow.png")

exit = False
cutscene = False
play = False

timer1 = Objects.timer(12, False)
timer2 = Objects.timer(5, False)
timer3 = Objects.timer(5, False)
timer4 = Objects.timer(5, False)
timer5 = Objects.timer(4.5, False)

spooky = pygame.mixer.Sound("Audio/microscope.wav")

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, cutscene, play, spooky
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    selected = Objects.getSelected()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if selected != "Blue" or cutscene:
                    exit = True

    if selected == "Blue":
        if not cutscene:
            Player.cutscene = True
            if not play:
                Sounds.powerAmb.stop()
                spooky.play()
                play = True
            virtual_screen.blit(eye1, (0,0))
            timer1.setInitial()
            if timer1.Done():
                virtual_screen.blit(eye2, (0,0))
                timer2.setInitial()
                if timer2.Done():
                    virtual_screen.blit(eye3, (0,0))
                    timer3.setInitial()
                    if timer3.Done():
                        virtual_screen.blit(eye4, (0,0))
                        timer4.setInitial()
                        if timer4.Done():
                            virtual_screen.blit(eye5, (0,0))
                            timer5.setInitial()
                            if timer5.Done():
                                Sounds.powerAmb.play(-1)
                                exit = True
                                cutscene = True
                                Player.cutscene = False
        else:
            virtual_screen.blit(blue, (0,0))
    elif selected == "Red":
        virtual_screen.blit(red, (0,0))
    elif selected == "Yellow":
        virtual_screen.blit(yellow, (0,0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale