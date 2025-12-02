import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player

virtual_res = (288, 1000)
# virtual_res = (288, 115)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False

heroBackground = pygame.image.load("Assets/creditsScreenHERO.png")
darkBackground = pygame.image.load("Assets/creditsScreenDARK.png")
evilBackground = pygame.image.load("Assets/creditsScreenEVIL.png")

background = evilBackground

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

scroll = Objects.timer(0.05, True) # TODO: make the scroll less headache inducing
ypos = 860

done = False

submerge = Sounds.loadAudio("Audio/submerge.wav")
submerge.set_volume(0.1)
submergeTimer = Objects.timer(11, False)

def inBounds(x, y):
    global exit, tooDark
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    global background
    print("credits")
    if Player.ending == "dark":
        background = darkBackground
    elif Player.ending == "hero":
        background = heroBackground

def Room(screen, screen_res, events):
    global exit, startMusic, ts2, ts3, repeat, ts4, ts5, repeat2, hover, count, clicked, ypos, done
    xScale = screen.get_width()/288
    yScale = screen.get_height()/140

    for event in events:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = (mouse_x/xScale, mouse_y/yScale)

    virtual_screen.blit(background, (0,0))

    virtual_view = virtual_screen.subsurface((0, ypos, 288, 140))

    scaled = pygame.transform.scale(virtual_view, screen_res)
    screen.blit(scaled, (0, 0))

    if not startMusic:
        print("starting credits scroll")
        startMusic = True
        gap.initial_time = pygame.time.get_ticks()
        scroll.initial_time = pygame.time.get_ticks()

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

    # Begin scroll up
    if scroll.Done():
        if ypos == 0:
            scroll.initial_time = -1
            done = True
        else:
            ypos -= 1
            scroll.initial_time = pygame.time.get_ticks()

    # Begin game
    if done:
        exit = True

    return player_pos, xScale, yScale