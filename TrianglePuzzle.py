import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import random

virtual_res = (750,500)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

exit = False
played = False
gaveup = False
cutscene = False

timer1 = Objects.timer(5, False)
timer2 = Objects.timer(10, False)

trianglePuzzle = {
    1: 11,
    2: 10,
    3: 4,
    4: 3,
    5: 7,
    6: 12,
    7: 5,
    8: 2,
    9: 1,
    10: 8,
    11: 13,
    12: 6,
    13: 9,
    14: 14
}

triangles = {}
for i in range(17):
    triangles[i+1] = pygame.image.load(f"Assets/Triangle{i+1}.png")

giveup = pygame.image.load("Assets/giveup.png")
opentriangle = pygame.image.load("Assets/opentriangle.png")
eye = pygame.image.load("Assets/triangleEye.png")
scaledEye = pygame.transform.scale(eye, (eye.get_width()*2, eye.get_height()))
lucky = pygame.image.load("Assets/lucky.png")
expected = pygame.image.load("Assets/expected.png")

opentriangleSound = pygame.mixer.Sound("Audio/opentriangle.wav")
girlLaughing = pygame.mixer.Sound("Audio/girlLaughing.wav")
girlLaughing.set_volume(0.5)
clapping = pygame.mixer.Sound("Audio/clapping.wav")

giveupRect = pygame.Rect(190, 410, giveup.get_width(), giveup.get_height())

gridPos = {
    1: (80,100),
    2: (150,98),
    3: (220,100),
    4: (290,98),
    5: (360,100),
    6: (430,98),
    7: (500,100),
    8: (80,224),
    9: (150,226),
    10: (220,224),
    11: (290,226),
    12: (360,224),
    13: (430,226),
    14: (500,224)
}

triangleHitboxes = {
    1: Polygon([(92, 233),(241, 233),(159,114)]),
    2: Polygon([(241, 233),(159,114),(308,114)]),
    3: Polygon([(241, 233),(390,233),(308,114)]),
    4: Polygon([(457,114),(390,233),(308,114)]),
    5: Polygon([(457,114),(390,233),(539,233)]),
    6: Polygon([(457,114),(606,114),(539,233)]),
    7: Polygon([(688,233),(606,114),(539,233)]),
    8: Polygon([(92, 233),(241, 233),(159,352)]),
    9: Polygon([(241, 233),(159,352),(308,352)]),
    10: Polygon([(241, 233),(390,233),(308,352)]),
    11: Polygon([(457,352),(390,233),(308,352)]),
    12: Polygon([(457,352),(390,233),(539,233)]),
    13: Polygon([(457,352),(606,352),(539,233)]),
    14: Polygon([(688,233),(606,352),(539,233)])
}

def getTriangle(triangle, pos):
    triangleType = triangle % 2
    posType = pos % 2
    if triangle == 14:
        if posType == 0:
            return triangles[14], gridPos[pos]
        return triangles[17], gridPos[pos]
    if triangleType != posType and triangle:
        if posType == 0:
            return triangles[16], gridPos[pos]
        return triangles[15], gridPos[pos]
    angleFactor = (triangle-pos)/2
    if triangle <= 7 and pos > 7:
        angleFactor -= 1
    if triangle > 7 and pos <= 7:
        angleFactor += 1
    if triangleType == 0:
        if angleFactor % 3 == -1:
            shift = (-20, -10)
        if angleFactor % 3 == -2:
            shift = (-42, -12)
        if angleFactor % 3 == 1:
            shift = (-5, -75)
        if angleFactor % 3 == 2:
            shift = (-56, -73)
        if angleFactor % 3 == 0:
            shift = (0,0)
    else:
        if angleFactor % 3 == -1:
            shift = (35, 45)
        if angleFactor % 3 == -2:
            shift = (-52, 43)
        if angleFactor % 3 == 1:
            shift = (-40, -15)
        if angleFactor % 3 == 2:
            shift = (-21, -13)
        if angleFactor % 3 == 0:
            shift = (0,0)
    finalPos = (gridPos[pos][0] + shift[0], gridPos[pos][1] + shift[1])

    rotatedTriangle = pygame.transform.rotate(triangles[triangle], 120 * angleFactor)
    return rotatedTriangle, finalPos

def Switch(pos):
    if trianglePuzzle[1] == 14:
        if pos in (2,8,10):
            trianglePuzzle[1] = trianglePuzzle[pos]
            trianglePuzzle[pos] = 14
            return True
        return False
    for i in range(2, 7):
        if trianglePuzzle[i] == 14:
            if pos % 2 == 0:
                if pos in (i-1,i+1,i+5,i+7,i+9):
                    trianglePuzzle[i] = trianglePuzzle[pos]
                    trianglePuzzle[pos] = 14
                    return True
            if pos in (i-1,i+1,i+7):
                trianglePuzzle[i] = trianglePuzzle[pos]
                trianglePuzzle[pos] = 14
                return True
    if trianglePuzzle[7] == 14:
        if pos in (6,12,14):
            trianglePuzzle[7] = trianglePuzzle[pos]
            trianglePuzzle[pos] = 14
            return True
    if trianglePuzzle[8] == 14:
        if pos in (1,3,9):
            trianglePuzzle[8] = trianglePuzzle[pos]
            trianglePuzzle[pos] = 14
            return True
    for i in range(9, 14):
        if trianglePuzzle[i] == 14:
            if pos % 2 != 0:
                if pos in (i-1,i+1,i-5,i-7,i-9):
                    trianglePuzzle[i] = trianglePuzzle[pos]
                    trianglePuzzle[pos] = 14
                    return True
            if pos in (i-1,i+1,i-7):
                trianglePuzzle[i] = trianglePuzzle[pos]
                trianglePuzzle[pos] = 14
                return True
    if trianglePuzzle[14] == 14:
        if pos in (5,7,13):
            trianglePuzzle[14] = trianglePuzzle[pos]
            trianglePuzzle[pos] = 14 
            return True
    return False

letterRect = pygame.Rect(230, 420, 130, 60)
magnet = 0
solved = False
collected = False

def inBounds(x, y):
    global exit
    if exit:
        exit = False
        return 0
    return False

def positionDeterminer(cameFrom):
    pass

def Room(screen, screen_res, events):
    global magnet, girlLaughing, exit, solved, collected, timer1, timer2, played, gaveup, cutscene
    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, _ = Objects.getPinkWingInfo()
    lit = (upperWingPower and level == 1 and power) or Objects.getPinkPower()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and not cutscene:
                exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                scaled_mouse_x = mouse_x / xScale
                scaled_mouse_y = mouse_y / yScale
                if lit and not solved:
                    if giveupRect.collidepoint(scaled_mouse_x, scaled_mouse_y):
                        solved = True
                        gaveup = True
                        clapping.play()
                        timer2.setInitial()
                        for key in trianglePuzzle:
                            trianglePuzzle[key] = key
                    pos = None
                    for key, hitbox in triangleHitboxes.items():
                        if hitbox.contains(Point(scaled_mouse_x, scaled_mouse_y)):
                            pos = key
                            break
                    if pos != None:
                        if Switch(pos):
                            magnet = random.randint(0,2)
                            Sounds.magnets[magnet].play()

                            solved = True
                            for i, triangle in trianglePuzzle.items():
                                #print("i:", i, "triangle", triangle, "\n")
                                if i != triangle:
                                    solved = False
                            if solved and not gaveup:
                                girlLaughing.play()
                elif letterRect.collidepoint((scaled_mouse_x, scaled_mouse_y)):
                    opentriangleSound.play()
                    collected = True
                    
    virtual_screen.fill((185, 122, 87))
    dark_overlay.fill((0, 0, 0, 150))

    for i in range(1,15):
        triangle, pos = getTriangle(trianglePuzzle[i], i)
        virtual_screen.blit(triangle, pos)

    pygame.draw.circle(virtual_screen, (255, 201, 14), (0,0), 35)
    pygame.draw.circle(virtual_screen, (255, 201, 14), (750,0), 35)
    pygame.draw.circle(virtual_screen, (255, 201, 14), (0,500), 35)
    pygame.draw.circle(virtual_screen, (255, 201, 14), (750,500), 35)

    if not solved:
        virtual_screen.blit(giveup, (190, 410))
    else:
        virtual_screen.blit(giveup, (190, 410))
        cutscene = True
        if not gaveup:
            timer1.setInitial()
            virtual_screen.blit(lucky, (5,5))
        else:
            virtual_screen.blit(expected, (-10,5))
        virtual_screen.blit(scaledEye, (95,142))
        if timer1.Done() or timer2.Done():
            cutscene = False
            if not played:
                opentriangleSound.play()
                played = True
            virtual_screen.blit(opentriangle, (190, 410))
            if not collected:
                pygame.draw.rect(virtual_screen, (195,195,195), (230, 420, 130, 60))
                pygame.draw.rect(virtual_screen, "black", (230, 420, 130, 60), 1)
                pygame.draw.line(virtual_screen, "black", (270, 450), (320, 430), 3)
                pygame.draw.line(virtual_screen, "black", (270, 450), (320, 470), 3)
                pygame.draw.line(virtual_screen, "black", (295, 440), (295, 460), 3)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale