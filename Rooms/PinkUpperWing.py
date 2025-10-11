import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff


virtual_res = (324, 219)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_res2 = (420, 219)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay2 = pygame.Surface(virtual_screen2.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(239, 180)

bounds = Polygon([(39, 102), (294, 102), (305, 174), (25, 174)])

trianglePuzzle1 = False
trianglePuzzle2 = False
whiteboard = False
beaker = False
table = False
trianglePuzzle1Rect = pygame.Rect(35, 102, 60, 6)
trianglePuzzle2Rect = pygame.Rect(225, 102, 60, 6)
whiteboardRect = pygame.Rect(92, 102, 133, 6)
beakerRect = pygame.Rect(20, 135, 30, 50)
beakerboundRect = Polygon([(13,180),(26,176),(50,125),(13, 125)])
tableRect = pygame.Rect(99, 125, 124, 24)
tableboundRect = pygame.Rect(99, 149, 124, 6)

exitRect = pygame.Rect(220, 188, 35, 20)
exitWalk = pygame.Rect(220, 174, 35, 34)

lights = [
    Objects.SquishedLight(257, 180, 1),
    Objects.SquishedLight(68, 180, 1),
    Objects.SquishedLight(185, 180, 1),
    Objects.SquishedLight(126, 180, 1),
    Objects.SquishedLight(221, 111, 1),
    Objects.SquishedLight(94, 111, 1),
    Objects.SquishedLight(158, 111, 1)
]
light_pos = (70, 50)
light_pos2 = (240, 50)
wall_lights = [
    LightSource(light_pos[0], light_pos[1], radius=60, strength = 220),
    LightSource(light_pos2[0], light_pos2[1], radius=60, strength = 220)
]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

background = pygame.image.load("Assets/PinkUpperWing.png")
door = pygame.image.load("Assets/pinkupperwingdoor.png")
powerdoor = pygame.image.load("Assets/powerdoor.png")
whiteboardimg = pygame.image.load("Assets/whiteboard.png")
whiteboardzoom = pygame.image.load("Assets/whiteboardzoom.png")
tripuzzle = pygame.image.load("Assets/tripuzzle.png")
tripuzzlesolved = pygame.image.load("Assets/tripuzzlesolved.png")
tripuzzlehints = pygame.image.load("Assets/tripuzzlehints.png")
mscopetable = pygame.image.load("Assets/mscopetable.png")
smolRed = pygame.image.load("Assets/smolRed.png")
smolYellow = pygame.image.load("Assets/smolYellow.png")
smolBlue = pygame.image.load("Assets/smolBlue.png")
circleLightUnscaled = pygame.image.load("Assets/CircleLight.png")
circleLight = pygame.transform.scale(circleLightUnscaled, (22, 22))
tableWidth = mscopetable.get_width()/3
tableHeight = mscopetable.get_height()/3
mscopetableScale = pygame.transform.scale(mscopetable, (tableWidth, tableHeight))
beakercase = pygame.image.load("Assets/beakers.png")
beakercase2 = pygame.image.load("Assets/beakers2.png")
tooDarkReadScale = pygame.transform.scale(Assets.tooDarkRead, (Assets.tooDarkRead.get_width()/1.25,Assets.tooDarkRead.get_height()/1.25))
tooDarkRead = Objects.briefText(virtual_screen, tooDarkReadScale, 10, 180, 3)
tooDarkSeeScale = pygame.transform.scale(Assets.tooDarkSee, (Assets.tooDarkSee.get_width()/1.25,Assets.tooDarkSee.get_height()/1.25))
tooDarkSee = Objects.briefText(virtual_screen, tooDarkSeeScale, 15, 180, 3)


def inBounds(x, y):
    global trianglePuzzle1, trianglePuzzle2, beaker, tableRect, table, tooDarkRead
    if exitRect.collidepoint((x,y)):
        level, power = Objects.getPipeDungeonInfo()
        upperWingPower, _ = Objects.getPinkWingInfo()
        if level == 1 and power and not upperWingPower and not Objects.getPinkPower():
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        tooDarkRead.activated_time = -1
        tooDarkSee.activated_time = -1
        return 0
    elif trianglePuzzle2:
        trianglePuzzle2 = False
        return 1
    elif trianglePuzzle1:
        trianglePuzzle1 = False
        return 2
    elif beaker:
        beaker = False
        return 3
    elif table:
        table = False
        return 4
    elif exitWalk.collidepoint(x,y):
        return True
    elif whiteboard:
        return False
    elif tableRect.collidepoint(x,y):
        return False
    elif beakerboundRect.contains(Point(x,y)):
        return False
    elif not bounds.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.PinkRoom":
        player_pos = pygame.Vector2(exitWalk.centerx + 2, exitWalk.centery - 5)



def Room(screen, screen_res, events):
    global trianglePuzzle1, trianglePuzzle2, whiteboard, beaker, table, tableboundRect, tooDarkRead

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()
    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = (upperWingPower and level == 1 and power) or Objects.getPinkPower()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if whiteboardRect.collidepoint(player_pos):
                    tooDarkSee.activated_time = -1
                    tooDarkRead.activated_time = pygame.time.get_ticks()
                elif trianglePuzzle2Rect.collidepoint(player_pos) or trianglePuzzle1Rect.collidepoint(player_pos) or beakerRect.collidepoint(player_pos) or tableboundRect.collidepoint(player_pos):
                    tooDarkRead.activated_time = -1
                    tooDarkSee.activated_time = pygame.time.get_ticks()
                if lit:
                    if trianglePuzzle2Rect.collidepoint(player_pos):
                        trianglePuzzle2 = True
                    if trianglePuzzle1Rect.collidepoint(player_pos):
                        trianglePuzzle1 = True
                    if whiteboardRect.collidepoint(player_pos):
                        whiteboard = True
                    if beakerRect.collidepoint(player_pos):
                        beaker = True
                    if tableboundRect.collidepoint(player_pos):
                        table = True
            if event.key == pygame.K_BACKSPACE:
                if whiteboard:
                    whiteboard = False

    virtual_screen.blit(background, (0,0))
    virtual_screen2.fill((195, 195, 195))
    if not lit:
        dark_overlay.fill((0, 0, 0, 150))
        dark_overlay2.fill((0, 0, 0, 150))



    #if lit:
       # Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))
      #  Assets.punch_light_hole(virtual_screen2, dark_overlay2, (virtual_screen2.get_width()/2, virtual_screen2.get_height()/2), 500, (100, 0, 100))

    virtual_screen.blit(tripuzzlehints, (43,66))
    virtual_screen.blit(whiteboardimg, (99,43))

    if not Objects.getTriangleSolved():
        virtual_screen.blit(tripuzzle, (232,66))
    else:
        virtual_screen.blit(tripuzzlesolved, (232,66))
    virtual_screen.blit(powerdoor, (31,188))
    virtual_screen.blit(door, (221,188))

    for i in range(6):
        virtual_screen.blit(Assets.squishedPipes2[1], (64 + 36*i, 180))

    for i in range(4):
        virtual_screen.blit(Assets.squishedPipes2[1], (100 + 36*i, 111))

    for i in range(9):
        virtual_screen.blit(Assets.squishedPipes2[2], (218, 173 - 7*i))

    #virtual_screen.blit(Assets.squishedPipes2[0], (218, 180))
    virtual_screen.blit(Assets.squishedPipes2[4], (28, 180))

    for light in lights:
        if lit:
            light.image = Assets.squishedTiles[1]
        else:
            light.image = Assets.squishedDimTiles[1]
        virtual_screen.blit(pygame.transform.scale(light.image, (36, 8)), light.rect)

    if player_pos.y > 125:
        virtual_screen.blit(mscopetableScale, (105, 100))
        if Objects.getBeakerSolved():
            virtual_screen.blit(beakercase2, (10, 70))
        else:
            virtual_screen.blit(beakercase, (10, 70))
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)
    else:
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)
        virtual_screen.blit(mscopetableScale, (105, 100))
        if Objects.getBeakerSolved():
            virtual_screen.blit(beakercase2, (10, 70))
        else:
            virtual_screen.blit(beakercase, (10, 70))
    virtual_screen.blit(circleLight, circleLight.get_rect(center=light_pos))
    virtual_screen.blit(circleLight, circleLight.get_rect(center=light_pos2))

    virtual_screen2.blit(whiteboardzoom, (20,20))

    red, yellow, blue = Objects.getColorsPlaced()

    if red:
        virtual_screen.blit(smolRed, (150, 121))
    if yellow:
        virtual_screen.blit(smolYellow, (160, 120))
    if blue:
        virtual_screen.blit(smolBlue, (157, 124))

    
    if not lit and not Objects.getPinkPower():
        tooDarkRead.update()
        tooDarkSee.update()

    if not lit:
        virtual_screen.blit(dark_overlay, (0, 0))
        virtual_screen2.blit(dark_overlay2, (0, 0))
    else:
        apply_lighting(virtual_screen, wall_lights, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
        apply_falloff(falloff, virtual_screen, light_pos)
        apply_falloff(falloff, virtual_screen, light_pos2)

    if not whiteboard:
        Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)
    else:
        Assets.scaled_draw(virtual_res, virtual_screen2, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
