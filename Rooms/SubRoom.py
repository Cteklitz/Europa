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
import random

virtual_res = (648,357)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

virtual_res2 = (388, 343)
virtual_screen2 = pygame.Surface(virtual_res2)
dark_overlay2 = pygame.Surface(virtual_screen2.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(239, 180)

fertilizer = pygame.image.load("Assets/Fertilizer.png")
fertilizer_pos = (20, 90)

rake = pygame.image.load("Assets/Rake.png")
rake_pos = (45, 75)

waterCan = pygame.image.load("Assets/WaterCan.png")
waterCan_pos = (15, 120)

fuelLine = Assets.fuelLine
fuelLineFixed = Assets.fuelLineFixed
fuelLinePos = (34, 167)
puddle = Assets.fuelPuddle
puddlePos = (270,226)
puddleUpper = Assets.fuelPuddleUpper
puddleUpperPos = (300,207)

fuelLineInteractRect = pygame.Rect(270, 200, 80, 50)
consoleInteractRect = pygame.Rect(415, 134, 153, 134)

eyeOpen = pygame.transform.scale(pygame.image.load("Assets/EyeWall.png"), (120, 85))
eyeClosed = pygame.transform.scale(pygame.image.load("Assets/eyeClosedWall.png"), (120, 85))

eyeOpenSmall = pygame.transform.scale(pygame.image.load("Assets/EyeWall.png"), (30, 22))
eyeClosedSmall = pygame.transform.scale(pygame.image.load("Assets/eyeClosedWall.png"), (30, 22))

eye_rect = pygame.Rect(0, 0, eyeOpen.get_width(), 100)
eye_rect2 = pygame.Rect(0, 0, 30, 22)

eyes = [eyeOpen, eyeClosed]
eyes2 = [eyeOpenSmall, eyeClosedSmall]
currEye = eyes[0]
currEye2 = eyes2[1]
currIndex = 0
currIndex2 = 0

added = False

influence = pygame.image.load("Assets/influence.png")
hero1 = pygame.image.load("Assets/hero1.png")
hero2 = pygame.image.load("Assets/hero2.png")
hero3 = pygame.image.load("Assets/hero3.png")
whyshouldi = Objects.briefText(virtual_screen, Assets.whyshouldi, 15, 180, 3)

animationIndex = 0

animationTimer = Objects.timer(2.5, False)
lighterTimer = Objects.timer(1.5, False)

cutscene1 = False
cutscene2 = False
brainwashPlayed = False
lighterPlayed = False
explosionPlayed = False

smallEyesPositions = [
    (231, 40),
    (261, 91),
    (261, 141),
    (231, 177),
    (113, 177),
    (83, 141),
    (83, 91),
    (113, 40),
    (204, 53),      
    (237, 118),     
    (204, 168),     
    (140, 168), 
    (107, 118),
    (140, 53),
    (172, 72),
    (172, 151)
]

firstTime = pygame.time.get_ticks()
firstTime2 = pygame.time.get_ticks()
nextBlinkDelay = random.randint(3000, 5000)
nextBlinkDelay2 = random.randint(3000, 5000)
bounds = Polygon([(32,224),(0,287),(227,280),(453,247),(453,224)])

lit = False
light_pos = (70, 50)
light_pos2 = (240, 50)
wall_lights = [
    LightSource(light_pos[0], light_pos[1], radius=60, strength = 220),
    LightSource(light_pos2[0], light_pos2[1], radius=60, strength = 220)
]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 140)]

# load assets
background = pygame.image.load("Assets/SubRoom.png")
exitRect = pygame.Rect(4, 175, 21, 115)

fixed = False
explode = False
leave = False

def inBounds(x, y):
    if explode: 
        #return 1 
        pass
    elif leave:
        #return 2
        pass

    elif Player.cutscene:
        return False
    elif exitRect.collidepoint((x,y)):
        Sounds.whispers.stop()
        return 0
    elif not bounds.contains(Point(x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos, added
    if not added:
        if Player.events != 0:
            Player.events += 1
        added = True
    if cameFrom == "Rooms.YellowHallway":
        Sounds.whispers.play(-1)
        player_pos = pygame.Vector2(exitRect.centerx + 35, exitRect.centery + 25)

def Room(screen, screen_res, events):
    global firstTime, currIndex, nextBlinkDelay, currEye, firstTime2, currIndex2, currEye2, nextBlinkDelay2, smallEyesPositions, fixed, cutscene1, cutscene2, \
        animationIndex, lighterPlayed, explosionPlayed, brainwashPlayed
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    currTime = pygame.time.get_ticks()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if fuelLineInteractRect.collidepoint(player_pos) and Player.checkItem(Items.electricalTape) and not fixed:
                    if Player.events != 6:
                        fixed = True
                        Sounds.tape.play()
                    else:
                        whyshouldi.activated_time = pygame.time.get_ticks()
                elif fuelLineInteractRect.collidepoint(player_pos) and Player.checkItem(Items.lighter) and not (cutscene1 or cutscene2) and not fixed:
                    if Player.events != 6:
                        Player.cutscene = True
                        animationTimer.setInitial()
                        virtual_screen2.blit(influence, (0,0))
                        Sounds.brainwash.play()
                        if Player.events == 0:
                            cutscene1 = True
                        else:
                            cutscene2 = True
                    else:
                        whyshouldi.activated_time = pygame.time.get_ticks()
                elif consoleInteractRect.collidepoint(player_pos) and fixed:
                    leave = True
                elif consoleInteractRect.collidepoint(player_pos) and not fixed:
                    # maybe something to imply sub cannot go without repair?
                    pass

    virtual_screen.blit(background, (0,0))

    if fixed:
        virtual_screen.blit(fuelLineFixed, fuelLinePos)
        virtual_screen.blit(puddle, puddlePos)
    else:
        virtual_screen.blit(fuelLine, fuelLinePos)
        virtual_screen.blit(puddle, puddlePos)
        virtual_screen.blit(puddleUpper, puddleUpperPos)


    if (currTime - firstTime2 >= nextBlinkDelay2) and not Player.cutscene:
            currIndex2 = (currIndex2 + 1) % len(eyes2)
            currEye2 = eyes2[currIndex2] # sets current eye for animation in array
            firstTime2 = currTime
            if currIndex2 == 1: # closed eye
                nextBlinkDelay2 = random.randint(70, 120)
                Sounds.blink.play()
            else: # open eye
                nextBlinkDelay2 = random.randint(2000, 5000)
    for position in smallEyesPositions:    
        virtual_screen.blit(currEye2, position, eye_rect2)

    if (currTime - firstTime >= nextBlinkDelay) and not Player.cutscene:
        currIndex = (currIndex + 1) % len(eyes)
        currEye = eyes[currIndex] # sets current eye for animation in array
        firstTime = currTime
        if currIndex == 1: # closed eye
            nextBlinkDelay = random.randint(70, 120)
            Sounds.blink.play()
        else: # open eye
            nextBlinkDelay = random.randint(2000, 5000)
    virtual_screen.blit(currEye, (130, 80), eye_rect)           

    Player.animatePlayer(virtual_screen, player_pos)

    apply_lighting(virtual_screen, wall_lights, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
    apply_falloff(falloff, virtual_screen, light_pos)

    if animationTimer.Done() and cutscene1:
        if animationIndex == 0:
            virtual_screen2.blit(hero1, (0,0))
        elif animationIndex == 1:
            virtual_screen2.blit(hero2, (0,0))
        elif animationIndex == 2:
            lighterTimer.setInitial()
            virtual_screen2.blit(hero3, (0,0))
        else:
            if not explosionPlayed:
                Sounds.brainwash.stop()
                Sounds.whispers.stop()
                Sounds.explosion2.play()
                explosionPlayed = True
                virtual_screen2.fill("black")
                # TODO: make this true when explosion noise ends
                explode = True
        animationIndex += 1
        animationTimer.reset()
        animationTimer.setInitial()

    if lighterTimer.Done() and not lighterPlayed:
        Sounds.lighter.play()
        lighterPlayed = True

    if animationTimer.Done() and cutscene2:
        Sounds.brainwash.stop()
        Player.cutscene = False

    whyshouldi.update()

    if Player.cutscene:
        Assets.scaled_draw(virtual_res2, virtual_screen2, screen_res, screen)
    else:
        Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3.5, 3.5  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
