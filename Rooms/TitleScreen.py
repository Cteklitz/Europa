import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds

virtual_res = (288, 450)
# virtual_res = (288, 115)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False

titleScreen = pygame.image.load("Assets/titleScreen1.png")
titleScreen2 = pygame.image.load("Assets/titleScreen2.png")
titleScreen3 = pygame.image.load("Assets/titleScreen3.png")
titleScreen4 = pygame.image.load("Assets/titleScreen4.png")
titleScreen5 = pygame.image.load("Assets/titleScreen5.png")

startMusic = False 
ts2 = False
ts3 = False
repeat = True

ts4 = False
ts5 = False
repeat2 = True

gap = Objects.timer(4, False)
gap2 = Objects.timer(0.5, False)
blip = Objects.timer(0.4, False)
blip2 = Objects.timer(0.4, False)

selectedStart = pygame.image.load("Assets/selectedStart.png")
startRect = pygame.Rect(179,58,53,17)
hover = False

click = Objects.timer(0.1, True)
count = 0
clicked = False

scroll = Objects.timer(0.0175, True)
ypos = 0

submerge = pygame.mixer.Sound("Audio/submerge.wav")
submerge.set_volume(0.1)
submergeTimer = Objects.timer(11, False)

def inBounds(x, y):
    global exit, tooDark
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global exit, startMusic, ts2, ts3, repeat, ts4, ts5, repeat2, hover, count, clicked, ypos
    xScale = screen.get_width()/288
    yScale = screen.get_height()/140

    for event in events:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = (mouse_x/xScale, mouse_y/yScale)
        if event.type == pygame.MOUSEMOTION and not clicked:
            if startRect.collidepoint(mouse_pos):
                hover = True
            else:
                hover = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not clicked:
            if event.button == 1:
                if startRect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()
                    submerge.play()
                    click.initial_time = pygame.time.get_ticks()
                    submergeTimer.initial_time = pygame.time.get_ticks()

    virtual_screen.blit(titleScreen, (0,0))

    if ts2:
        virtual_screen.blit(titleScreen2, (0,0))
    if ts3:
        virtual_screen.blit(titleScreen3, (0,0))
    if ts4:
        virtual_screen.blit(titleScreen4, (0,0))
    if ts5:
        virtual_screen.blit(titleScreen5, (0,0))

    if hover:
        virtual_screen.blit(selectedStart, startRect)

    virtual_view = virtual_screen.subsurface((0, ypos, 288, 140))

    scaled = pygame.transform.scale(virtual_view, screen_res)
    screen.blit(scaled, (0, 0))

    if not startMusic:
        pygame.mixer.music.load("Audio/wading_into_the_unknown.wav")
        pygame.mixer.music.set_volume(0.08)
        pygame.mixer.music.play(-1) 
        startMusic = True
        gap.initial_time = pygame.time.get_ticks()

    # Jupiter blip
    if gap.Done():
        ts2 = True
        gap.initial_time = -1
        blip.initial_time = pygame.time.get_ticks()
    elif blip.Done():
        if repeat:
            ts2 = False
            ts3 = True
            blip.initial_time = pygame.time.get_ticks()
            repeat = False
        else:
            ts3 = False
            blip.initial_time = -1
            gap.initial_time = pygame.time.get_ticks()
            gap2.initial_time = pygame.time.get_ticks()
            repeat = True

    # Title blip
    if gap2.Done():
        ts4 = True
        gap2.initial_time = -1
        blip2.initial_time = pygame.time.get_ticks()
    elif blip2.Done():
        if repeat2:
            ts4 = False
            ts5 = True
            blip2.initial_time = pygame.time.get_ticks()
            repeat2 = False
        else:
            ts5 = False
            blip2.initial_time = -1
            gap2.initial_time = -1
            repeat2 = True

    # Button flicker on click
    if click.Done():
        count += 1
        hover = not hover
        if count < 3:
            click.initial_time = pygame.time.get_ticks()
        if count == 3:
            click.initial_time = -1
            scroll.initial_time = pygame.time.get_ticks()

    # Begin scroll down
    if scroll.Done():
        if ypos == virtual_screen.get_height() - 140:
            scroll.initial_time = -1
        else:
            ypos += 1
            scroll.initial_time = pygame.time.get_ticks()

    # Begin game
    if submergeTimer.Done():
        exit = True

    return player_pos, xScale, yScale