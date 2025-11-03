import pygame
import Assets
import Objects
from shapely.geometry import Point, Polygon
import Sounds
import Player
import Items

virtual_res = (416, 256)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)

player_pos = pygame.Vector2(192, 128)

ladderHatchOpen_original = pygame.image.load("Assets/LadderHatchOpen.png")

original_size = ladderHatchOpen_original.get_size()
new_size = (int(original_size[0] * 0.40), int(original_size[1] * 0.3))
ladderHatchOpen = pygame.transform.scale(ladderHatchOpen_original, new_size)

# Load puddle images
puddle1 = pygame.image.load("Assets/Puddle1.png")
puddle2 = pygame.image.load("Assets/Puddle2.png")
puddle3 = pygame.image.load("Assets/Puddle3.png")

# puddle positions
puddle1_pos = (270, 140)  # Position puddle1 bottom
puddle2_pos = (270, 80)   # Position puddle2 top
puddle3_pos = (280, 110)  # Position puddle3 middle

# puddle interaction region
puddleRegion = pygame.Rect(250, 70, 60, 80)  

lowerLevelFlooded = pygame.image.load("Assets/LowerLevelFlooded.png")
lowerLevelFloodedText = Objects.briefText(virtual_screen, lowerLevelFlooded, 15, 180, 3)

# puddle interaction variables
puddleSelected = False

hatchPosition = (90, 40)
hatchRect = pygame.Rect(hatchPosition[0], hatchPosition[1], new_size[0], new_size[1])  # Clickable area

bounds = Polygon([(48,48), (368,48), (368,208), (48,208)])

lights = [
    Objects.Light(336, 80, 2),
    Objects.Light(336, 144, 2),
    Objects.Light(48, 48, 2),
    Objects.Light(48, 176, 2)
]

southDoor = Objects.Door((virtual_screen.get_width()/2) - 16, 208, Assets.grayDoorSouth)
westDoor = Objects.Door(16, 112, Assets.grayDoorWest)
eastDoor = Objects.Door(368, 112, Assets.grayDoorEast)
topRightWall = pygame.Rect(275, 48, 125, 31)
bottomRightWall = pygame.Rect(276, 176, 124, 32)

powerRoom = False

def inBounds(x, y):
    global powerRoom, puddleSelected

    level, power = Objects.getPipeDungeonInfo()
    if southDoor.rect.collidepoint((x,y)):
        lowerLevelFloodedText.activated_time = -1
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 0
    elif westDoor.rect.collidepoint((x,y)):
        lowerLevelFloodedText.activated_time = -1
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 1
    elif eastDoor.rect.collidepoint((x,y)):
        lowerLevelFloodedText.activated_time = -1
        if level == 2 and power:
            Sounds.powerAmb.stop()
            Sounds.ominousAmb.play(-1)
        return 2
    elif puddleSelected:
        puddleSelected = False
        return 4  
    elif powerRoom:
        if Objects.getBluePower():
            Sounds.powerOnAmb.play(-1)
        powerRoom = False
        return 3
    elif not bounds.contains(Point(x,y)) or topRightWall.collidepoint((x,y)) or bottomRightWall.collidepoint((x,y)):
        return False
    return True

def positionDeterminer(cameFrom):
    global player_pos
    if cameFrom == "Rooms.BreakerRoom":
        player_pos = pygame.Vector2(southDoor.x + 16, southDoor.y - 5)
    if cameFrom == "Rooms.StorageCloset":
        player_pos = pygame.Vector2(westDoor.x + 37, westDoor.y + 16)
    if cameFrom == "Rooms.ValvePuzzle":
        player_pos = pygame.Vector2(eastDoor.x - 5, eastDoor.y + 16)
    if cameFrom == "Rooms.BluePower":
        player_pos = pygame.Vector2(123, 75)

def Room(screen, screen_res, events):
    global powerRoom, puddleSelected
    level, power = Objects.getPipeDungeonInfo()

    for event in events:
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if hatchRect.collidepoint(player_pos):
                        if not Objects.getWaterLevelsSolved():
                            lowerLevelFloodedText.activated_time = pygame.time.get_ticks()
                        else:
                            powerRoom = True
                    
                    elif Player.checkItem(Items.mop):
                        if puddleRegion.collidepoint(player_pos):
                            puddleSelected = True

    virtual_screen.fill((105,105,105))
    dark_overlay.fill((0, 0, 0, 150))
    outerRect = pygame.Rect((16,16,384,224))
    innerRect = pygame.Rect((48,48,320,160))

    # outer walls
    pygame.draw.rect(virtual_screen, "gray", outerRect)
    pygame.draw.rect(virtual_screen, "black", outerRect, 1)
    pygame.draw.rect(virtual_screen, "black", innerRect, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.topleft, innerRect.topleft, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.topright, innerRect.topright, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.bottomleft, innerRect.bottomleft, 1)
    pygame.draw.line(virtual_screen, "black", outerRect.bottomright, innerRect.bottomright, 1)

    # hallway wall on bottom right
    pygame.draw.rect(virtual_screen, (105, 105, 105), (275, 176, 200, 200))
    pygame.draw.rect(virtual_screen, "black", (275, 176, 200, 200), 1)
    pygame.draw.line(virtual_screen, (105, 105, 105), (275,240), (275,256))
    pygame.draw.line(virtual_screen, (105, 105, 105), (400,176), (416,176))
    pygame.draw.rect(virtual_screen, "gray", bottomRightWall)
    pygame.draw.rect(virtual_screen, "black", bottomRightWall, 1)
    pygame.draw.line(virtual_screen, "gray", (398,176),(368,176), 2)
    pygame.draw.line(virtual_screen, "black", (399,207),(367,176))

    # hallway wall on top right
    pygame.draw.rect(virtual_screen, (105, 105, 105), (275, -120, 200, 200))
    pygame.draw.rect(virtual_screen, "black", (275, -120, 200, 200), 1)
    pygame.draw.line(virtual_screen, (105, 105, 105), (275,0), (275,15))
    pygame.draw.line(virtual_screen, (105, 105, 105), (400,79), (416,79))
    pygame.draw.rect(virtual_screen, "gray", topRightWall)
    pygame.draw.rect(virtual_screen, "black", topRightWall, 1)
    pygame.draw.line(virtual_screen, "gray", (398,78),(368,78), 2)
    pygame.draw.line(virtual_screen, "black", (399,48),(367,78))

    Done = False

    for light in lights:
        light.update()
        if not Done:
            #Assets.punch_light_hole(virtual_screen, dark_overlay, (112, 112), 300, (0, 162, 232))
            Done = True
        virtual_screen.blit(light.image, light.rect)

    for y in range(144, 208, 32):
        virtual_screen.blit(Assets.pipes[12], (int(virtual_screen.get_width()/2) - 16,y))

    virtual_screen.blit(Assets.pipes[15], (int(virtual_screen.get_width()/2) - 16,112))

    for x in range(int(virtual_screen.get_width()/2) + 16, 368, 32):
        virtual_screen.blit(Assets.pipes[10], (x,112))

    virtual_screen.blit(southDoor.image, southDoor.rect)
    virtual_screen.blit(westDoor.image, westDoor.rect)
    virtual_screen.blit(eastDoor.image, eastDoor.rect)

    virtual_screen.blit(ladderHatchOpen, hatchPosition)

    # Draw puddles
    virtual_screen.blit(puddle1, puddle1_pos)
    virtual_screen.blit(puddle2, puddle2_pos)
    virtual_screen.blit(puddle3, puddle3_pos)

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)

    lowerLevelFloodedText.update()

    #virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
