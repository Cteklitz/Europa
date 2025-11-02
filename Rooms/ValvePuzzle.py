# Example file showing a circle moving on screen
import pygame
import Assets
import Objects
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff

virtual_res = (352, 384)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 50))

player_pos = pygame.Vector2(175, 340)

floor = pygame.image.load("Assets/floor.png")
door = pygame.image.load("Assets/powerRoomDoor.png")
flippedDoor = pygame.transform.flip(door, True, False)
console = pygame.image.load("Assets/Doohickey.png")

dimLightScale1 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2, Assets.squishedDimTiles[1].get_height()*1.5))
dimLightScale2 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2.2, Assets.squishedDimTiles[1].get_height()*1.5))
dimLightScale3 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2.5, Assets.squishedDimTiles[1].get_height()*1.5))

LightScale1 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2, Assets.squishedTiles[1].get_height()*1.5))
LightScale2 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2.2, Assets.squishedTiles[1].get_height()*1.5))
LightScale3 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2.5, Assets.squishedTiles[1].get_height()*1.5))

lightPos = [(64 + 16,0 + 16), (256 + 16,0 + 16), (64 + 16,224 + 16), (256 + 16,224 + 16)]
lightsNew = [LightSource(lightPos[0][0], lightPos[0][1], radius=60, strength = 220),
             LightSource(lightPos[1][0], lightPos[1][1], radius=60, strength = 220),
             LightSource(lightPos[2][0], lightPos[2][1], radius=60, strength = 220),
             LightSource(lightPos[3][0], lightPos[3][1], radius=60, strength = 220),]
falloff = [LightFalloff((virtual_res[0], virtual_res[1]), darkness = 25)]   

def inBounds(x, y):
    doorRect = pygame.Rect(9,208,door.get_width(),door.get_height())
    consoleRect = pygame.Rect(int(virtual_screen.get_width()/2) - 64 - 16, 225, console.get_width() + 32, console.get_height())
    if doorRect.collidepoint(x,y):
        return 0
    if consoleRect.collidepoint(x,y):
        return False
    if y > 368:
        return False
    if x < 16 or x > 336:
        return False
    if x < 64:
        if y > 384 - (x + 64):
            return True
        return False
    if x >= 64 and x < 288:
        if y > 256:
            return True
        return False
    if x >= 288:
        if y > 384 - (352 - x + 64):
            return True
        return False
    
leftIndex = 0
rightIndex = 1
waterLevels = [30, 60, 75, 35]
solved = False

waterLevelSprites = Assets.load_tileset("Assets/waterLevels.png", 30, 155)
redArrow = pygame.image.load("Assets/redArrow.png")
greenArrow = pygame.image.load("Assets/greenArrow.png")

# def increaseLeftIndex():
#     global leftIndex, rightIndex
#     if leftIndex == 3:
#         if rightIndex == 0:
#             leftIndex = 1
#         else:
#             leftIndex = 0
#     else:
#         leftIndex += 1
#         if leftIndex == rightIndex:
#             leftIndex += 1
#             if leftIndex == 4:
#                 leftIndex = 0

# def increaseRightIndex():
#     global rightIndex, leftIndex
#     if rightIndex == 3:
#         if leftIndex == 0:
#             rightIndex = 1
#         else:
#             rightIndex = 0
#     else:
#         rightIndex += 1
#         if leftIndex == rightIndex:
#             rightIndex += 1
#             if rightIndex == 4:
#                 rightIndex = 0

# def switch15():
#     global waterLevels, leftIndex, rightIndex
#     if waterLevels[leftIndex] < waterLevels[rightIndex] and waterLevels[leftIndex] <= 85 and waterLevels[rightIndex] >= 15:
#         waterLevels[leftIndex] += 15
#         waterLevels[rightIndex] -= 15
#     elif waterLevels[rightIndex] < waterLevels[leftIndex] and waterLevels[rightIndex] <= 85 and waterLevels[leftIndex] >= 15:
#         waterLevels[rightIndex] += 15
#         waterLevels[leftIndex] -= 15

# def switch10():
#     global waterLevels, leftIndex, rightIndex
#     if waterLevels[leftIndex] < waterLevels[rightIndex] and waterLevels[leftIndex] <= 90 and waterLevels[rightIndex] >= 10:
#         waterLevels[leftIndex] += 10
#         waterLevels[rightIndex] -= 10
#     elif waterLevels[rightIndex] < waterLevels[leftIndex] and waterLevels[rightIndex] <= 90 and waterLevels[leftIndex] >= 10:
#         waterLevels[rightIndex] += 10
#         waterLevels[leftIndex] -= 10
# 
# valves = [
#     Objects.Valve(64, 300, increaseLeftIndex),
#     Objects.Valve(128, 300, increaseRightIndex),
#     Objects.Valve(192, 300, switch15),
#     Objects.Valve(256, 300, switch10)
# ]

def move15():
    global waterLevels
    if waterLevels[0] >= 15 and waterLevels[1] <= 85:
        waterLevels[0] = waterLevels[0] - 15
        waterLevels[1] = waterLevels[1] + 15

def move10():
    global waterLevels
    if waterLevels[1] >= 25 and waterLevels[3] <= 75:
        waterLevels[1] = waterLevels[1] - 25
        waterLevels[3] = waterLevels[3] + 25

def move5():
    global waterLevels
    if waterLevels[1] <= 95 and waterLevels[2] >= 5:
        waterLevels[2] = waterLevels[2] - 5
        waterLevels[1] = waterLevels[1] + 5

def split20():
    global waterLevels
    if waterLevels[3] >= 20 and waterLevels[0] <= 90 and waterLevels[2] <= 90:
        waterLevels[3] = waterLevels[3] - 20
        waterLevels[2] = waterLevels[2] + 10
        waterLevels[0] = waterLevels[0] + 10

valves = [
    Objects.Valve(64, 300, move15),
    Objects.Valve(128, 300, move10),
    Objects.Valve(192, 300, move5),
    Objects.Valve(256, 300, split20)
]

def positionDeterminer(cameFrom):
    global player_pos
    player_pos = pygame.Vector2(9 + flippedDoor.get_width(), 208 + (flippedDoor.get_height()*5/6))

def Room(screen, screen_res, events):
    global valves, redArrow, greenArrow, solved
    level, power = Objects.getPipeDungeonInfo()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for valve in valves:
                    valve.check_collision(player_pos)
                good = True
                for i in range(3):
                    if waterLevels[i] != 50:
                        good = False
                if good:
                    solved = True

    # fill the screen with a color to wipe away anything from last frame
    virtual_screen.fill("gray")
    dark_overlay.fill((0, 0, 0, 150))

    virtual_screen.blit(floor, (0, 256))
    pygame.draw.line(virtual_screen, (0,0,0), (64, 0), (64, 256), 1)
    pygame.draw.line(virtual_screen, (0,0,0), (288, 0), (288, 256), 1)

    if power and level == 2:
        virtual_screen.blit(Assets.tiles[2], (64,0))
        virtual_screen.blit(Assets.tiles[2], (256,0))
        virtual_screen.blit(Assets.tiles[2], (64,224))
        virtual_screen.blit(Assets.tiles[2], (256,224))
    else:
        virtual_screen.blit(Assets.dimTiles[2], (64,0))
        virtual_screen.blit(Assets.dimTiles[2], (256,0))
        virtual_screen.blit(Assets.dimTiles[2], (64,224))
        virtual_screen.blit(Assets.dimTiles[2], (256,224))

    virtual_screen.blit(Assets.pipes[16], (int(virtual_screen.get_width()/2) - 16,308))
    virtual_screen.blit(Assets.pipes[17], (int(virtual_screen.get_width()/2) - 16,276))
    virtual_screen.blit(Assets.pipes[12], (int(virtual_screen.get_width()/2) - 16,244))

    for x in range(int(virtual_screen.get_width()/2) - 48, 16, -32):
        virtual_screen.blit(Assets.pipes[10], (x,276))

    for x in range(int(virtual_screen.get_width()/2) - 48, 48, -32):
        virtual_screen.blit(Assets.pipes[10], (x,308))

    for x in range(int(virtual_screen.get_width()/2) + 16, 275, 32):
        virtual_screen.blit(Assets.pipes[10], (x,308))

    pygame.draw.line(virtual_screen, "black", (63,320), (63,328), 1)
    pygame.draw.line(virtual_screen, "black", (288,320), (288,328), 1)

    virtual_screen.blit(Assets.pipes[18], (8,276))

    virtual_screen.blit(console, (int(virtual_screen.get_width()/2) - 64,225))

    virtual_screen.blit(flippedDoor, (9,208))

    if player_pos.y < 312:
        pygame.draw.circle(virtual_screen, "red", player_pos, 16)

        for valve in valves:
            valve.update()
            virtual_screen.blit(valve.image, valve.rect)
    else:
        for valve in valves:
            valve.update()
            virtual_screen.blit(valve.image, valve.rect)

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    waterX = 88
    for i in range(4):
        imageIndex = int(waterLevels[i] / 5)
        virtual_screen.blit(waterLevelSprites[imageIndex], (waterX, 52))
        if waterLevels[i] == 50:
            virtual_screen.blit(greenArrow, (waterX-5, 125))
        else:
            virtual_screen.blit(redArrow, (waterX-5, 125))
        waterX += 49

        #for i in range(4, len(lightsNew)):
            #apply_falloff(falloff, virtual_screen, (lightsNew[i].x, lightsNew[i].y))

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
