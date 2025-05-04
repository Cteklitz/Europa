import pygame
import math

#Draws polygon from lower-right corner
def draw_polygon(surface, start_pos, numSides, length, color, width=1, fill=False):
    points = []
    angle_degrees = 360/numSides
    angle_radians = math.radians(angle_degrees)
    for i in range (numSides):
        end_x = start_pos[0] + length * math.cos(angle_radians)
        end_y = start_pos[1] - length * math.sin(angle_radians)
        end_pos = (end_x, end_y)
        points.append(start_pos)
        start_pos = end_pos
        angle_radians += math.radians(angle_degrees)
    
    if fill:
        pygame.draw.polygon(surface, color, points)
    else:
        pygame.draw.polygon(surface, color, points, width)

    return points

def punch_light_hole(surface, overlay, position, radius, color):
    light = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    hole = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(light, (*color, 200), (radius, radius), radius)
    pygame.draw.circle(hole, (0, 0, 0, 255), (radius, radius), radius)
    surface.blit(light, (position[0] - radius, position[1] - radius), special_flags=pygame.BLEND_RGBA_ADD)
    overlay.blit(hole, (position[0] - radius, position[1] - radius), special_flags=pygame.BLEND_RGBA_SUB)

def load_tileset(path, tile_width, tile_height):
    sheet = pygame.image.load(path)
    tiles = []
    sheet_width, sheet_height = sheet.get_size()
    for y in range(0, sheet_height, tile_height):
        for x in range(0, sheet_width, tile_width):
            rect = pygame.Rect(x, y, tile_width, tile_height)
            image = sheet.subsurface(rect)
            tiles.append(image)
    return tiles

tiles = load_tileset("Assets/Grid.png", 32, 32)
dimTiles = load_tileset("Assets/DimGrid.png", 32, 32)
pipes = load_tileset("Assets/PipeSet.png", 32, 32)
pinkSwitch= load_tileset("Assets/PinkSwitch.png", 32, 32)
orangeSwitch= load_tileset("Assets/OrangeSwitch.png", 32, 32)
blueSwitch= load_tileset("Assets/BlueSwitch.png", 32, 32)
greenSwitch= load_tileset("Assets/GreenSwitch.png", 32, 32)
valveSprites = load_tileset("Assets/Valve.png", 32, 32)

ctrlRoomDoor = pygame.image.load("Assets/CtrlRoomDoor.png")

orangeDoorNorth = pygame.image.load("Assets/OrangeDoor.png")
greenDoorSouth = pygame.image.load("Assets/GreenDoor.png")
pinkDoorWest = pygame.image.load("Assets/PinkDoor.png")
blueDoorEast = pygame.image.load("Assets/BlueDoor.png")

orangeDoorSouth = pygame.transform.flip(orangeDoorNorth, False, True)
greenDoorNorth = pygame.transform.flip(greenDoorSouth, False, True)
pinkDoorEast = pygame.transform.flip(pinkDoorWest, True, False)
blueDoorWest = pygame.transform.flip(blueDoorEast, True, False)

grayDoorEast = pygame.image.load("Assets/GrayDoor.png")
grayDoorWest = pygame.transform.flip(grayDoorEast, True, False)
grayDoorNorth = pygame.transform.rotate(grayDoorEast, 90)
grayDoorSouth = pygame.transform.rotate(grayDoorEast, -90)

bigBoygGrayDoorNorth = pygame.transform.scale(grayDoorNorth, (80,32))

squishedTiles = []
for i in range(5):
    squished = pygame.transform.scale(tiles[i], (80, 8))
    squishedTiles.append(squished)

squishedDimTiles = []
for i in range(5):
    squished = pygame.transform.scale(dimTiles[i], (80, 8))
    squishedDimTiles.append(squished)

squishedPipes = []
for i in range(12):
    squished = pygame.transform.scale(pipes[i], (80, 8))
    squishedPipes.append(squished)

tooDark = pygame.image.load("Assets/TooDark.png")