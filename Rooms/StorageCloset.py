# Example file showing a circle moving on screen
import pygame
import Assets
import Objects
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff

virtual_res = (176, 142)  # Reduced by 50%
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 50))

player_pos = pygame.Vector2(87.5, 30)  # Reduced by 50%

floor = pygame.image.load("Assets/floor_small.png")
print(f"{floor.get_width()}, {floor.get_height()}")
door = pygame.image.load("Assets/powerRoomDoor.png")

dimLightScale1 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/4, Assets.squishedDimTiles[1].get_height()*0.75))
dimLightScale2 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/4.4, Assets.squishedDimTiles[1].get_height()*0.75))
dimLightScale3 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/5, Assets.squishedDimTiles[1].get_height()*0.75))

LightScale1 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/4, Assets.squishedTiles[1].get_height()*0.75))
LightScale2 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/4.4, Assets.squishedTiles[1].get_height()*0.75))
LightScale3 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/5, Assets.squishedTiles[1].get_height()*0.75))

class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 1

lights = [
    [Light(78, 90), dimLightScale1, LightScale1],  # Reduced by 50%
    [Light(78, 86), dimLightScale1, LightScale1],
    [Light(78, 82), dimLightScale1, LightScale1],
    [Light(78, 78), dimLightScale1, LightScale1],
    [Light(78, 74), dimLightScale1, LightScale1],
    [Light(78, 70), dimLightScale1, LightScale1],
    [Light(78, 66), dimLightScale1, LightScale1],
    [Light(79, 62), dimLightScale2, LightScale2],
    [Light(80, 58), dimLightScale3, LightScale3]
]

lightPos = [(32 + 8, 0 + 8), (128 + 8, 0 + 8), (32 + 8, 62 + 8), (128 + 8, 62 + 8)]  # Reduced by 50%
lightsNew = [LightSource(lightPos[0][0], lightPos[0][1], radius=30, strength = 220),  # Radius reduced by 50%
             LightSource(lightPos[1][0], lightPos[1][1], radius=30, strength = 220),
             LightSource(lightPos[2][0], lightPos[2][1], radius=30, strength = 220),
             LightSource(lightPos[3][0], lightPos[3][1], radius=30, strength = 220),]
falloff = [LightFalloff((virtual_res[0], virtual_res[1]), darkness = 25)]
        

def inBounds(x, y):
    doorRect = pygame.Rect(150, 24, door.get_width(), door.get_height())  # Reduced by 50%
    if doorRect.collidepoint(x,y):
        return 0
    if y > 134:  # Reduced by 50%
        return False
    if x < 8 or x > 168:  # Reduced by 50%
        return False
    if x < 32:  # Reduced by 50%
        if y > 142 - (x + 32):  # Reduced by 50%
            return True
        return False
    if x >= 32 and x < 144:  # Reduced by 50%
        if y > 78:  # Reduced by 50%
            return True
        return False
    if x >= 144:  # Reduced by 50%
        if y > 142 - (176 - x + 32):  # Reduced by 50%
            return True
        return False

def positionDeterminer(cameFrom):
    global player_pos
    player_pos = pygame.Vector2(150 - 15 + door.get_width()/4, 24 + (door.get_height()*5/6))  # Reduced by 50%

def Room(screen, screen_res, events):
    level, power = Objects.getPipeDungeonInfo()

    # fill the screen with a color to wipe away anything from last frame
    virtual_screen.fill("gray")
    dark_overlay.fill((0, 0, 0, 150))

    pygame.draw.line(virtual_screen, (0,0,0), (31, 0), (31, 78), 1)  # Reduced by 50%
    pygame.draw.line(virtual_screen, (0,0,0), (144, 0), (144, 78), 1)  # Reduced by 50%
    virtual_screen.blit(floor, (0, 78))  # Reduced by 50%

    '''
    if power and level == 2:
        virtual_screen.blit(Assets.tiles[2], (32,0))  # Reduced by 50%
        virtual_screen.blit(Assets.tiles[2], (128,0))  # Reduced by 50%
        virtual_screen.blit(Assets.tiles[2], (32,62))  # Reduced by 50%
        virtual_screen.blit(Assets.tiles[2], (128,62))  # Reduced by 50%
    else:
        virtual_screen.blit(Assets.dimTiles[2], (32,0))  # Reduced by 50%
        virtual_screen.blit(Assets.dimTiles[2], (128,0))  # Reduced by 50%
        virtual_screen.blit(Assets.dimTiles[2], (32,62))  # Reduced by 50%
        virtual_screen.blit(Assets.dimTiles[2], (128,62))  # Reduced by 50%
    '''

    virtual_screen.blit(door, (150,24))  # Reduced by 50%

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)  # Reduced by 50%

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 3, 3  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)