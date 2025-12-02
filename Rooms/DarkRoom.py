import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player

virtual_res = (324, 219)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_res2 = (1195, 896)
virtual_screen2 = pygame.Surface(virtual_res2)

player_pos = pygame.Vector2(239, 180)

bounds = Polygon([(39, 102), (294, 102), (305, 174), (25, 174)])

# south exit
exitRect = pygame.Rect(247, 188, 58, 31)
exitWalk = pygame.Rect(247, 174, 58, 45)

# north exit
exitRect2 = pygame.Rect(192, 48, 59, 63)

falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

background = pygame.image.load("Assets/DarkRoom.png")
shadow = pygame.image.load("Assets/Shadow.png")
tooDarkScale = pygame.transform.scale(Assets.tooDark, (Assets.tooDark.get_width()/1.25,Assets.tooDark.get_height()/1.25))
tooDark = Objects.briefText(virtual_screen, tooDarkScale, 15, 180, 3)
noUseText = pygame.image.load("Assets/noUse.png")
noUse = Objects.briefText(virtual_screen, noUseText, 0, 150, 3)

animationIndex = 0

animation = []
for i in range(1, 16):
    animation.append(pygame.image.load(f"Assets/screenshot{i}.png"))

animationTimer = Objects.timer(0.75, False)

played = False
cutscene = False
credits = False

def inBounds(x, y):
    shadowBound = Polygon([(59,0),(0,0),(0,219),(259,219)])
    if credits:
        return 2
    elif exitRect.collidepoint((x,y)):
        tooDark.activated_time = -1
        if not Objects.getValvePlaced():
            return 0
    elif exitRect2.collidepoint((x,y)):
        tooDark.activated_time = -1
        noUse.activated_time = -1
        return 1
    elif exitWalk.collidepoint(x,y):
        if not Objects.getValvePlaced():
            return True
        else:
            tooDark.activated_time = -1
            noUse.activated_time = pygame.time.get_ticks()
    if not bounds.contains(Point(x,y)):
        return False
    elif shadowBound.contains(Point(x,y)):
        noUse.activated_time = -1
        tooDark.activated_time = pygame.time.get_ticks()
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos, played, cutscene, credits
    if not played:
        Sounds.whatAwaits.play(-1)
        played = True
    if Player.events == 6:
        cutscene = True
        animationTimer.setInitial()
    if cameFrom == "Rooms.YellowRoom":
        player_pos = pygame.Vector2(exitWalk.centerx + 2, exitWalk.centery - 20)
    if cameFrom == "Rooms.YellowHallway":
        player_pos = pygame.Vector2(exitRect2.x + exitRect2.width/2, exitRect2.y + 68)

def Room(screen, screen_res, events):
    global cutscene, animationIndex, credits

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = (upperWingPower and level == 1 and power) or Objects.getPinkPower()

    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

    virtual_screen.blit(background, (0,0))
    dark_overlay.fill((0, 0, 0, 200))

    Player.animatePlayer(virtual_screen, player_pos)

    virtual_screen.blit(shadow, (10,0))

    if cutscene:
        Player.cutscene = True
        Player.ending = "dark"
        virtual_screen2.fill("black")
        if animationIndex < 14:
            if animationTimer.Done():
                animationIndex += 1
                animationTimer.reset()
                animationTimer.setInitial()

            virtual_screen2.blit(animation[animationIndex], (0,0))

        if animationIndex == 14 and animationTimer.Done():
            credits = True

    virtual_screen.blit(dark_overlay, (0, 0))

    tooDark.update()
    noUse.update()

    if Player.events == 7:
        Assets.scaled_draw(virtual_res2, virtual_screen2, screen_res, screen)
    else:
        Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3.5, 3.5  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
