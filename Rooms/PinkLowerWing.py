import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon, LineString
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff

virtual_res = (904, 208)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(642, 112)

lights = [
    Objects.SquishedLight(80, 112, 1),
    Objects.SquishedLight(233, 112, 1),
    Objects.SquishedLight(376, 112, 1),
    Objects.SquishedLight(520, 112, 1),
    Objects.SquishedLight(680, 112, 1),
    Objects.SquishedLight(600, 184, 1),
    Objects.SquishedLight(440, 184, 1),
    Objects.SquishedLight(280, 184, 1),
    Objects.SquishedLight(120, 184, 1)
]

# Lighting
light_pos = (50, 50)
light_pos2 = (640, 50)
light_pos3 = (300, 50)
wall_lights = [
    LightSource(light_pos[0], light_pos[1], radius=60, strength = 220),
    LightSource(light_pos2[0], light_pos2[1], radius=60, strength = 220),
    LightSource(light_pos3[0], light_pos3[1], radius = 10, strength=220)
]
falloff = [LightFalloff(virtual_screen.get_size(), darkness = 70)]

bookcase = False
lDoor = False
desk = False
table = False

Bookcase = pygame.image.load("Assets/Bookcase.png")
Bookcase2 = pygame.image.load("Assets/Bookcase2.png")
Lit = pygame.image.load("Assets/WindowLit.png")
scaledLit = pygame.transform.scale(Lit, (396, 68))
unlit = pygame.image.load("Assets/WindowUnlit.png")
scaledUnlit = pygame.transform.scale(unlit, (396, 68))
lockedDoor = pygame.image.load("Assets/LockedDoor1.png")
lockedDoorRect = lockedDoor.get_rect(topleft=(31,95))
lockedDoorRange = pygame.Rect(lockedDoorRect.x, lockedDoorRect.y-10, lockedDoorRect.width+10, lockedDoorRect.height+10)
Desk = pygame.image.load("Assets/Desk.png")
Desk2 = pygame.image.load("Assets/Desk2.png")
scaledDesk = pygame.transform.scale(Desk, (Desk.get_width(), Desk.get_height()/2))
scaledDesk2 = pygame.transform.scale(Desk2, (Desk2.get_width(), Desk2.get_height()/2))
deskRange = pygame.Rect(100, 66, scaledDesk.get_width(), scaledDesk.get_height())
Table = pygame.image.load("Assets/lowerWingTable.png")
Table2 = pygame.image.load("Assets/lowerWingTable2.png")
scaledTable = pygame.transform.scale(Table, (Table.get_width()*1.5, Table.get_height()/1.2))
scaledTable2 = pygame.transform.scale(Table2, (Table2.get_width()*1.5, Table2.get_height()/1.2))
tableRect = pygame.Rect(212,138,430,30)
tableRect2 = pygame.Rect(292,110,350,45)
tableRange = pygame.Rect(292,160,350,16)
scaledTooDarkSee = pygame.transform.scale(Assets.tooDarkSee, (Assets.tooDarkSee.get_width()*1.5, Assets.tooDarkSee.get_height()/1.2))
tooDarkSee = Objects.briefText(virtual_screen, scaledTooDarkSee, 170, 160, 3)
circleLight = pygame.image.load("Assets/CircleLight.png")
scaledLightLeft = pygame.transform.scale(circleLight, (circleLight.get_width()*1.9, circleLight.get_height()/1.0))
scaledLightLeft = pygame.transform.rotate(scaledLightLeft, 30)
scaledLightRight = pygame.transform.scale(circleLight, (circleLight.get_width()*1.9, circleLight.get_height()/1.0))

def inBounds(x, y):
    global bookcase, lDoor, lockedDoor, desk, table

    level, power = Objects.getPipeDungeonInfo()
    _, lowerWingPower = Objects.getPinkWingInfo()

    bigBoyRect = pygame.Rect(600,80,80,20)
    bookcaseRect = pygame.Rect(800,148,96,48)
    deskRect = pygame.Rect(100,66,197,42)
    point = Point(x, y)
    leftBound = LineString([(16, 190), (80, 100)])
    rightBound = LineString([(887, 190), (819, 100)])
    if bigBoyRect.collidepoint((x,y)):
        if level == 1 and power and not lowerWingPower:
            Sounds.ominousAmb.stop()
            Sounds.powerAmb.play(-1)
        tooDarkSee.activated_time = -1
        return 0
    if bookcase:
        tooDarkSee.activated_time = -1
        bookcase = False
        return 1
    if lDoor:
        lDoor = False
        return 2
    if desk:
        desk = False
        return 3
    if table:
        table = False
        return 4
    if lockedDoorRect.collidepoint(x,y) and Objects.getOpen():
        if not Objects.getPinkPower() and level == 1 and power and lowerWingPower:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        if Objects.getPinkPower():
            Sounds.powerOnAmb.play(-1)
        return 5
    if 80 < x < 819 and y < 100:
        return False
    if y > 176:
        return False
    if leftBound.distance(point) < 10 or rightBound.distance(point) < 10:
        return False
    if bookcaseRect.collidepoint((x,y)):
        return False
    if deskRect.collidepoint((x,y)):
        return False
    if tableRect.collidepoint((x,y)) or tableRect2.collidepoint((x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    bigBoyRect = pygame.Rect(600,80,80,20)
    if cameFrom == "Rooms.PinkPower":
        player_pos = pygame.Vector2(lockedDoorRect.x + lockedDoorRect.width + 20, lockedDoorRect.y + (lockedDoorRect.height*3/4))
    if cameFrom == "Rooms.LockedDoor":
        player_pos = pygame.Vector2(lockedDoorRect.x + lockedDoorRect.width + 20, lockedDoorRect.y + (lockedDoorRect.height*3/4))
    if cameFrom == "Rooms.PinkRoom":
        player_pos = pygame.Vector2(bigBoyRect.x + bigBoyRect.width/2, bigBoyRect.y + bigBoyRect.height + 5)

def Room(screen, screen_res, events):
    global bookcase, Bookcase, lDoor, desk, table

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    upperWingPower, lowerWingPower = Objects.getPinkWingInfo()

    bookcaseRange = pygame.Rect(792,140,104,56)

    _, _, blueFound = Objects.getColorsFound()

    spotdiffssolved = Objects.getSpotDiffsSolved()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if bookcaseRange.collidepoint(player_pos):
                    bookcase = True
                if lockedDoorRange.collidepoint(player_pos):
                    if not Objects.getOpen():
                        lDoor = True
                if deskRange.collidepoint(player_pos):
                    if level == 1 and power and lowerWingPower or Objects.getPinkPower():
                        desk = True
                    else:
                        tooDarkSee.activated_time = pygame.time.get_ticks()
                if tableRange.collidepoint(player_pos):
                    if level == 1 and power and lowerWingPower or Objects.getPinkPower():
                        table = True
                    else:
                        tooDarkSee.activated_time = pygame.time.get_ticks()

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))

    pygame.draw.rect(virtual_screen, "gray", (16, 0, 872, 192))
    pygame.draw.rect(virtual_screen, "black", (16, 0, 872, 192), 1)

    pygame.draw.rect(virtual_screen, "gray", (80, 0, 744, 112))
    pygame.draw.rect(virtual_screen, "black", (80, 0, 744, 112), 1)

    pygame.draw.line(virtual_screen, "black", (16, 190), (80, 112))
    pygame.draw.line(virtual_screen, "black", (887, 190), (824, 112))

    virtual_screen.blit(scaledLightLeft, scaledLightLeft.get_rect(center=light_pos))
    virtual_screen.blit(scaledLightRight, scaledLightLeft.get_rect(center=light_pos2))

    if (lowerWingPower and power and level == 1) or Objects.getPinkPower():
        Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (0, 0, 0))

    # Shows unlit window or lit depending on if lights are on
    if (lowerWingPower and power and level == 1) or Objects.getPinkPower():
        virtual_screen.blit(scaledLit, (83, 22))
    else:
        virtual_screen.blit(scaledUnlit, (83, 22))

    for x in range(160, 680, 80):
        virtual_screen.blit(Assets.squishedPipes[10], (x,112))

    for x in range(160, 600, 80):
        virtual_screen.blit(Assets.squishedPipes[10], (x,184))

    virtual_screen.blit(Assets.squishedPipes[0], (600,112))

    for y in range(120, 184, 8):
        virtual_screen.blit(Assets.squishedPipes[7], (600,y))

    pygame.draw.line(virtual_screen, "black", (628,112), (628,115), 3)
    pygame.draw.line(virtual_screen, "black", (651,112), (651,115), 3)

    virtual_screen.blit(Assets.squishedPipes[8], (12,142))
    virtual_screen.blit(Assets.squishedPipes[6], (80,142))

    for index, light in enumerate(lights):
        lit = light.update()
        if (lowerWingPower or Objects.getPinkPower()) and lit:
            light.image = Assets.squishedTiles[1]

        else:
            light.image = Assets.squishedDimTiles[1]
        virtual_screen.blit(light.image, light.rect)

    for y in range(120, 144, 8):
        virtual_screen.blit(Assets.squishedPipes[7], (80,y))

    if not blueFound:
        virtual_screen.blit(scaledDesk, (100,66))
    else:
        virtual_screen.blit(scaledDesk2, (100,66))

    virtual_screen.blit(Assets.bigBoygGrayDoorNorth, (600,80,80,32))
    letterCount = Objects.getLetterCount()
    if Objects.getOpen():
        letterCount = 5
    lockedDoor = pygame.image.load(f"Assets/LockedDoor{letterCount+1}.png")
    virtual_screen.blit(lockedDoor, (31, 95, lockedDoor.get_width(),lockedDoor.get_height()))

    circle_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, "red", (16, 16), 16)

    scaled_circle = pygame.transform.scale(circle_surface, (80, 32))

    if(player_pos.y >= 143):
        if not spotdiffssolved:
            virtual_screen.blit(scaledTable, (220,65))
        else:
            virtual_screen.blit(scaledTable2, (220,65))

    if(player_pos.y < 148):
        virtual_screen.blit(scaled_circle, (player_pos.x - 40, player_pos.y - 16))
        if not Objects.getCutscene():
            virtual_screen.blit(Bookcase, (800,100,96,96))
        else:
            virtual_screen.blit(Bookcase2, (800,100,96,96))
    else:
        if not Objects.getCutscene():
            virtual_screen.blit(Bookcase, (800,100,96,96))
        else:
            virtual_screen.blit(Bookcase2, (800,100,96,96))
        virtual_screen.blit(scaled_circle, (player_pos.x - 40, player_pos.y - 16))

    if(player_pos.y < 143):
        if not spotdiffssolved:
            virtual_screen.blit(scaledTable, (220,65))
        else:
            virtual_screen.blit(scaledTable2, (220,65))

    litSave = virtual_screen.subsurface((80, 31, 384, 64)).copy()

    virtual_screen.blit(dark_overlay, (0, 0))

    if not lit or not Objects.getPinkPower():
        tooDarkSee.update()

    # apply lighting (it will looks weird due to the screwy scaling in this room, way too much effort to fix it so whatever)
    if (lowerWingPower and power and level == 1) or Objects.getPinkPower():
        apply_lighting(virtual_screen, wall_lights, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
        apply_falloff(falloff, virtual_screen, (light_pos[0], light_pos[1]))
        apply_falloff(falloff, virtual_screen, light_pos2)

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale