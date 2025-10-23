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

dimLightScale1 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2, Assets.squishedDimTiles[1].get_height()*1.5))
dimLightScale2 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2.2, Assets.squishedDimTiles[1].get_height()*1.5))
dimLightScale3 = pygame.transform.scale(Assets.squishedDimTiles[1], (Assets.squishedDimTiles[1].get_width()/2.5, Assets.squishedDimTiles[1].get_height()*1.5))

LightScale1 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2, Assets.squishedTiles[1].get_height()*1.5))
LightScale2 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2.2, Assets.squishedTiles[1].get_height()*1.5))
LightScale3 = pygame.transform.scale(Assets.squishedTiles[1], (Assets.squishedTiles[1].get_width()/2.5, Assets.squishedTiles[1].get_height()*1.5))

class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 1

lights = [
    [Light(156, 180), dimLightScale1, LightScale1],
    [Light(156, 172), dimLightScale1, LightScale1],
    [Light(156, 164), dimLightScale1, LightScale1],
    [Light(156, 156), dimLightScale1, LightScale1],
    [Light(156, 148), dimLightScale1, LightScale1],
    [Light(156, 140), dimLightScale1, LightScale1],
    [Light(156, 132), dimLightScale1, LightScale1],
    [Light(158, 124), dimLightScale2, LightScale2],
    [Light(160, 116), dimLightScale3, LightScale3]
]

lightPos = [(64 + 16,0 + 16), (256 + 16,0 + 16), (64 + 16,224 + 16), (256 + 16,224 + 16)]
lightsNew = [LightSource(lightPos[0][0], lightPos[0][1], radius=60, strength = 220),
             LightSource(lightPos[1][0], lightPos[1][1], radius=60, strength = 220),
             LightSource(lightPos[2][0], lightPos[2][1], radius=60, strength = 220),
             LightSource(lightPos[3][0], lightPos[3][1], radius=60, strength = 220),]
falloff = [LightFalloff((virtual_res[0], virtual_res[1]), darkness = 25)]   

def inBounds(x, y):
    doorRect = pygame.Rect(9,208,door.get_width(),door.get_height())
    if doorRect.collidepoint(x,y):
        return 0
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

def positionDeterminer(cameFrom):
    global player_pos
    player_pos = pygame.Vector2(9 + flippedDoor.get_width(), 208 + (flippedDoor.get_height()*5/6))

def Room(screen, screen_res, events):
    level, power = Objects.getPipeDungeonInfo()

    # poll for events
    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

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

    virtual_screen.blit(flippedDoor, (9,208))

    pygame.draw.circle(virtual_screen, "red", player_pos, 16)

        #for i in range(4, len(lightsNew)):
            #apply_falloff(falloff, virtual_screen, (lightsNew[i].x, lightsNew[i].y))

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
