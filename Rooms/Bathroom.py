import pygame
import Assets
import Objects
import Items
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
closedToiletStall = pygame.image.load("Assets/toiletStallClosed.png")
openToiletStall = pygame.image.load("Assets/toiletStallOpen.png")
toilet = pygame.image.load("Assets/toilet.png")
closedShowerStall = pygame.image.load("Assets/showerStallClosed.png")
openShowerStall = pygame.image.load("Assets/showerStallOpen.png")
mirror = pygame.image.load("Assets/Mirror.png")
bathroomSink = pygame.image.load("Assets/BathroomSink.png")
bathroomSinkOn = pygame.image.load("Assets/BathroomSinkOn.png")
bleach = pygame.image.load("Assets/bleachGround.png")
tooDarkReadScale = pygame.transform.scale(Assets.tooDarkRead, (Assets.tooDarkRead.get_width()/1.25,Assets.tooDarkRead.get_height()/1.25))
tooDarkRead = Objects.briefText(virtual_screen, tooDarkReadScale, 10, 180, 3)
tooDarkSeeScale = pygame.transform.scale(Assets.tooDarkSee, (Assets.tooDarkSee.get_width()/1.25,Assets.tooDarkSee.get_height()/1.25))
tooDarkSee = Objects.briefText(virtual_screen, tooDarkSeeScale, 15, 180, 3)

# position and state for toilet stalls
toiletStallOpen1 = False
toiletStallPos1 = (150, 38)
toiletPos1 = (152, 69)
toiletStallOpen2 = False
toiletStallPos2 = (109, 38)
toiletPos2 = (111, 69)

# position and state for shower stalls
showerStallOpen1 = False
showerStallPos1 = (68 ,38)
showerStallOpen2 = False
showerStallPos2 = (27, 38)

#position and state for sinks
sinkOn1 = False
sinkPos1 = (206, 80)
sinkOn2 = False
sinkPos2 = (246, 80)

bleach = Objects.groundItem(showerStallPos2[0] + 8, showerStallPos2[1] + 66, Items.bleach)

# interact rects
toilet1InteractRect = pygame.Rect(toiletStallPos1[0], toiletStallPos1[1], 50, 95)
toilet2InteractRect = pygame.Rect(toiletStallPos2[0], toiletStallPos2[1], 50, 95)
shower1InteractRect = pygame.Rect(showerStallPos1[0], showerStallPos1[1], 50, 95)
shower2InteractRect = pygame.Rect(showerStallPos2[0], showerStallPos2[1], 50, 95)
sink1InteractRect = pygame.Rect(sinkPos1[0], sinkPos1[1], bathroomSink.get_width(), bathroomSink.get_height())
sink2InteractRect = pygame.Rect(sinkPos2[0], sinkPos2[1], bathroomSink.get_width(), bathroomSink.get_height())



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
    global trianglePuzzle1, trianglePuzzle2, whiteboard, beaker, table, tableboundRect, tooDarkRead, toiletStallOpen1, toiletStallOpen2, showerStallOpen1, showerStallOpen2, sinkOn1, sinkOn2

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    for event in events:

        # opens and closes stall doors
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if (showerStallOpen2 and not bleach.collected):
                    Sounds.pickup.play()
                    bleach.check_collision(player_pos)
                elif toilet1InteractRect.collidepoint(player_pos):
                    Sounds.openClose.play()
                    toiletStallOpen1 = not toiletStallOpen1
                elif toilet2InteractRect.collidepoint(player_pos):
                    Sounds.openClose.play()
                    toiletStallOpen2 = not toiletStallOpen2
                elif shower1InteractRect.collidepoint(player_pos):
                    Sounds.curtain.play()
                    showerStallOpen1 = not showerStallOpen1
                elif shower2InteractRect.collidepoint(player_pos):
                    Sounds.curtain.play()
                    showerStallOpen2 = not showerStallOpen2
                elif sink1InteractRect.collidepoint(player_pos):
                    if (not sinkOn1):
                        Sounds.sink.play(loops = -1)
                        sinkOn1 = True
                    else:
                        Sounds.sink.stop()
                        sinkOn1 = False
                elif sink2InteractRect.collidepoint(player_pos):
                    if (not sinkOn2):
                        Sounds.sink2.play(loops = -1)
                        sinkOn2 = True
                    else:
                        Sounds.sink2.stop()
                        sinkOn2 = False
                
                
            
    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = (upperWingPower and level == 1 and power) or Objects.getPinkPower()

    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

    virtual_screen.blit(background, (0,0))
    virtual_screen.blit(toilet, toiletPos1)
    virtual_screen.blit(toilet, toiletPos2)
    Objects.groundItem.draw(bleach, virtual_screen)

    # draws open or closed stalls depending on state
    if (not toiletStallOpen1):
        virtual_screen.blit(closedToiletStall, toiletStallPos1)
    else:
        virtual_screen.blit(openToiletStall, toiletStallPos1)
    if (not toiletStallOpen2):
        virtual_screen.blit(closedToiletStall, toiletStallPos2)
    else:
        virtual_screen.blit(openToiletStall, toiletStallPos2)
    if (not showerStallOpen1):
        virtual_screen.blit(closedShowerStall, showerStallPos1)
    else:
        virtual_screen.blit(openShowerStall, showerStallPos1)
    if (not showerStallOpen2):
        virtual_screen.blit(closedShowerStall, showerStallPos2)
    else:
        virtual_screen.blit(openShowerStall, showerStallPos2)
    if (not sinkOn1):
        virtual_screen.blit(bathroomSink, sinkPos1)
    else:
        virtual_screen.blit(bathroomSinkOn, sinkPos1)
    if (not sinkOn2):
        virtual_screen.blit(bathroomSink, sinkPos2)
    else:
        virtual_screen.blit(bathroomSinkOn, sinkPos2)
    virtual_screen.blit(mirror, (206, 47))
    
    
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
