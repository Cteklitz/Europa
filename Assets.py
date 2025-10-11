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

def draw_text(surface, text, color, rect, font):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "

        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y_offset = 0
    for line in lines:
        line_surf = font.render(line, True, color)
        surface.blit(line_surf, (rect.x, rect.y + y_offset))
        y_offset += font.get_height()


# properly scale aspect ratios, center
def scaled_draw(virtual_res, virtual_screen, screen_res, screen):
    # normalize aspect ratio for screen display
    room_ratio = virtual_res[0] / virtual_res[1]
    screen_res = (screen_res[1] * room_ratio, screen_res[1])  # effectively (sresy*vresx)/vresy, sresy

    # get user screen dimensions
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    black_back = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)  # fullscreen black background
    black_back.fill((0, 0, 0))
    screen.blit(black_back, (0, 0))

    center_x = (screen_w - screen_res[0]) // 2  # distance from left side to center

    # scale and center room
    scaled = pygame.transform.scale(virtual_screen, screen_res)
    screen.blit(scaled, (center_x, 0))


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

lockedDoorEast = pygame.image.load("Assets/LockedDoor.png")
lockedDoorWest = pygame.transform.flip(lockedDoorEast, True, False)
lockedDoorNorth = pygame.transform.rotate(lockedDoorEast, 90)
lockedDoorSouth = pygame.transform.rotate(lockedDoorEast, -90)

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
for i in range(14):
    squished = pygame.transform.scale(pipes[i], (80, 11))
    squishedPipes.append(squished)

squishedPipes2 = []
for i in range(14):
    squished = pygame.transform.scale(pipes[i], (41, 11))
    squishedPipes2.append(squished)

tooDarkRead = pygame.image.load("Assets/TooDark.png")
tooDarkSee = pygame.image.load("Assets/TooDarkSee.png")

letterTiles = load_tileset("Assets/letters.png", 21, 41)
numberTiles = load_tileset("Assets/numbers.png", 21, 41)

useButton = pygame.image.load("Assets/useButton.png")

### ITEMS
pinkKeycard = pygame.image.load("Assets/pink_keycard.png")
pinkKeycardGround = pygame.image.load("Assets/pink_keycard_ground.png")

bandage = pygame.image.load("Assets/bandage.png")
bandageGround = pygame.image.load("Assets/bandage_ground.png")

redPetri = pygame.image.load("Assets/redpetri.png")
redPetriGround = pygame.image.load("Assets/smolRed.png")
bluePetri = pygame.image.load("Assets/bluePetri.png")
bluePetriGround = pygame.image.load("Assets/smolblue.png")
yellowPetri = pygame.image.load("Assets/yellowPetri.png")
yellowPetriGround = pygame.image.load("Assets/smolyellow.png")

letterTile = pygame.image.load("Assets/letter_tile.png")