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

virtual_res2 = (400, 219)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay2 = pygame.Surface(virtual_screen2.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(239, 180)

bounds = Polygon([(19,110),(298,110),(308,181), (308,203), (16,203), (16,181)])

exitRect = pygame.Rect(304, 141, 10, 44)

light_pos = (70, 50)
light_pos2 = (240, 50)
wall_lights = [
    LightSource(light_pos[0], light_pos[1], radius=60, strength = 220),
    LightSource(light_pos2[0], light_pos2[1], radius=60, strength = 220)
]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

# load and scale assets
background = pygame.image.load("Assets/Bathroom.png")
closedStall = pygame.image.load("Assets/toiletStallClosed.png")
openStall = pygame.image.load("Assets/toiletStallOpen.png")
toilet = pygame.image.load("Assets/toilet.png")
mirror = pygame.image.load("Assets/Mirror.png")
bathroomSink = pygame.image.load("Assets/BathroomSink.png")
tooDarkReadScale = pygame.transform.scale(Assets.tooDarkRead, (Assets.tooDarkRead.get_width()/1.25,Assets.tooDarkRead.get_height()/1.25))
tooDarkRead = Objects.briefText(virtual_screen, tooDarkReadScale, 10, 180, 3)
tooDarkSeeScale = pygame.transform.scale(Assets.tooDarkSee, (Assets.tooDarkSee.get_width()/1.25,Assets.tooDarkSee.get_height()/1.25))
tooDarkSee = Objects.briefText(virtual_screen, tooDarkSeeScale, 15, 180, 3)

#positional and state for toilet stalls
stallOpen1 = False
stallPos1 = (154, 38)
toiletPos1 = (156, 69)
stallOpen2 = False
stallPos2 = (113, 38)
toiletPos2 = (115, 69)

def inBounds(x, y):
    global tooDarkRead
    if exitRect.collidepoint((x,y)):
        level, power = Objects.getPipeDungeonInfo()
        upperWingPower, _ = Objects.getPinkWingInfo()
        if level == 1 and power and not upperWingPower and not Objects.getPinkPower():
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        tooDarkRead.activated_time = -1
        tooDarkSee.activated_time = -1
        return 0
    elif not bounds.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.GreenRoom":
        player_pos = pygame.Vector2(exitRect.centerx - 15, exitRect.centery + 10)

def Room(screen, screen_res, events):
    global trianglePuzzle1, trianglePuzzle2, whiteboard, beaker, table, tableboundRect, tooDarkRead, stallOpen1, stallOpen2

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    for event in events:
        # opens and closes toilet stall doors
        if event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = event.pos
                click_x_unscaled = click_x/xScale
                click_y_unscaled = click_y/yScale
                if (159 < click_x_unscaled < 197 and  42 < click_y_unscaled < 124):
                    if (stallOpen1 == False):
                        stallOpen1 = True
                    else:
                        stallOpen1 = False
                elif (121 < click_x_unscaled < 159 and  42 < click_y_unscaled < 124):
                    if (stallOpen2 == False):
                        stallOpen2 = True
                    else:
                        stallOpen2 = False
    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = (upperWingPower and level == 1 and power) or Objects.getPinkPower()

    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

    virtual_screen.blit(background, (0,0))
    virtual_screen.blit(toilet, toiletPos1)
    virtual_screen.blit(toilet, toiletPos2)

    # draws open or closed stalls depending on state
    if (not stallOpen1):
        virtual_screen.blit(closedStall, stallPos1)
    else:
        virtual_screen.blit(openStall, stallPos1)
    if (not stallOpen2):
        virtual_screen.blit(closedStall, stallPos2)
    else:
        virtual_screen.blit(openStall, stallPos2)
    
    virtual_screen.blit(mirror, (210, 47))
    
    virtual_screen.blit(bathroomSink, (210, 80))
    virtual_screen.blit(bathroomSink, (250, 80))
    
    virtual_screen2.fill((195, 195, 195))
    if not lit:
        dark_overlay.fill((0, 0, 0, 150))
        dark_overlay2.fill((0, 0, 0, 150))

    Player.animatePlayer(virtual_screen, player_pos)
    
    if not lit and not Objects.getPinkPower():
        tooDarkRead.update()
        tooDarkSee.update()

    if not lit:
        virtual_screen.blit(dark_overlay, (0, 0))
        virtual_screen2.blit(dark_overlay2, (0, 0))
    else:
        apply_lighting(virtual_screen, wall_lights, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
        apply_falloff(falloff, virtual_screen, light_pos)

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3.5, 3.5  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
