import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon, LineString

virtual_res = (904, 208)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(600, 112)

bounds = Assets.draw_polygon(virtual_screen, (208, 208), 4, 160, "gray")
outline = Polygon(bounds)

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

pinkDoor = Objects.Door(208, 112, Assets.pinkDoorEast)
northDoor = Objects.Door(112, 16, Assets.grayDoorNorth)
southDoor = Objects.Door(112, 208, Assets.grayDoorSouth)

bookcase = False

def inBounds(x, y):
    global bookcase
    bigBoyRect = pygame.Rect(600,80,80,32)
    bookcaseRect = pygame.Rect(800,148,96,48)
    point = Point(x, y)
    leftBound = LineString([(16, 190), (80, 112)])
    rightBound = LineString([(887, 190), (824, 112)])
    if bigBoyRect.collidepoint((x,y)):
        return 0
    if bookcase:
        bookcase = False
        return 1
    if 80 < x < 824 and y < 112:
        return False
    if y > 176:
        return False
    if leftBound.distance(point) < 10 or rightBound.distance(point) < 10:
        return False
    if bookcaseRect.collidepoint((x,y)):
        return False
    return True

Bookcase = pygame.image.load("Assets/Bookcase.png")

def Room(screen, screen_res, events):
    global bookcase, Bookcase

    xScale = screen.get_width()/virtual_screen.get_width() 
    yScale = screen.get_height()/virtual_screen.get_height()

    level, power = Objects.getPipeDungeonInfo()
    _, lowerWingPower = Objects.getPinkWingInfo()

    bookcaseRange = pygame.Rect(792,140,104,56)

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if bookcaseRange.collidepoint(player_pos):
                    bookcase = True

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))

    pygame.draw.rect(virtual_screen, "gray", (16, 0, 872, 192))
    pygame.draw.rect(virtual_screen, "black", (16, 0, 872, 192), 1)

    pygame.draw.rect(virtual_screen, "gray", (80, 0, 744, 112))
    pygame.draw.rect(virtual_screen, "black", (80, 0, 744, 112), 1)

    pygame.draw.line(virtual_screen, "black", (16, 190), (80, 112))
    pygame.draw.line(virtual_screen, "black", (887, 190), (824, 112))

    if lowerWingPower and power and level == 1:
        Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/2, virtual_screen.get_height()/2), 500, (100, 0, 100))

    pygame.draw.rect(virtual_screen, (105,105,105), (80, 0, 384, 32))
    pygame.draw.rect(virtual_screen, "black", (80, 0, 384, 32), 1)

    pygame.draw.rect(virtual_screen, (105,105,105), (80, 95, 384, 17))
    pygame.draw.rect(virtual_screen, "black", (80, 95, 384, 17), 1)

    pygame.draw.rect(virtual_screen, "navyblue", (80, 31, 384, 64))
    pygame.draw.rect(virtual_screen, "black", (80, 31, 384, 64), 1)

    pygame.draw.rect(virtual_screen, (105,105,185), (104, 39, 360, 40))
    pygame.draw.rect(virtual_screen, "black", (104, 39, 360, 40), 1)

    pygame.draw.line(virtual_screen, (185, 122, 167), (133, 79), (133, 93))
    pygame.draw.line(virtual_screen, (185, 122, 167), (163, 79), (163, 93))

    pygame.draw.line(virtual_screen, (185, 122, 167), (316, 79), (316, 93))
    pygame.draw.line(virtual_screen, (185, 122, 167), (346, 79), (346, 93))

    pygame.draw.rect(virtual_screen, (0, 0, 30), (104, 50, 360, 20))
    pygame.draw.rect(virtual_screen, "black", (104, 50, 360, 20), 1)

    pygame.draw.line(virtual_screen, "white", (100, 60), (125, 35))
    pygame.draw.line(virtual_screen, "white", (160, 75), (185, 50))

    for x in range(160, 680, 80):
        virtual_screen.blit(Assets.squishedPipes[10], (x,112))

    for x in range(160, 600, 80):
        virtual_screen.blit(Assets.squishedPipes[10], (x,184))

    virtual_screen.blit(Assets.squishedPipes[0], (600,112))

    for y in range(120, 184, 8):
        virtual_screen.blit(Assets.squishedPipes[7], (600,y))

    for index, light in enumerate(lights):
        lit = light.update()
        if lowerWingPower and lit:
            light.image = Assets.squishedTiles[1]
            if index < 3:
                Assets.punch_light_hole(virtual_screen, dark_overlay, (light.x + 40, light.y + 6), 23, light.color)
                Assets.punch_light_hole(virtual_screen, dark_overlay, (light.x + 25, light.y + 8), 23, light.color)
                Assets.punch_light_hole(virtual_screen, dark_overlay, (light.x + 55, light.y + 8), 23, light.color)
        else:
            light.image = Assets.squishedDimTiles[1]
        virtual_screen.blit(light.image, light.rect)

    virtual_screen.blit(Assets.bigBoygGrayDoorNorth, (600,80,80,32))

    circle_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, "red", (16, 16), 16)

    scaled_circle = pygame.transform.scale(circle_surface, (80, 32))

    if(player_pos.y < 148):
        virtual_screen.blit(scaled_circle, (player_pos.x - 40, player_pos.y - 16))
        virtual_screen.blit(Bookcase, (800,100,96,96))
    else:
        virtual_screen.blit(Bookcase, (800,100,96,96))
        virtual_screen.blit(scaled_circle, (player_pos.x - 40, player_pos.y - 16))

    virtual_screen.blit(dark_overlay, (0, 0))

    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (0, 0))

    return player_pos, xScale, yScale