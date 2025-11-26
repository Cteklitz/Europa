# Example file showing a circle moving on screen
import pygame
import Assets
import Objects
import Sounds
from LightSource import LightSource
from LightFalloff import LightFalloff
from LightingUtils import apply_lighting, apply_falloff
import Player

greenPower = False
played = False

switchSound = Sounds.loadAudio("Audio/switch.wav")

powerSoundTimer = Objects.timer(1.5, False)
pulseTimer = Objects.timer(0.099, True)

virtual_res = (352, 384)
virtual_screen = pygame.Surface(virtual_res)
dark_overlay = pygame.Surface(virtual_screen.get_size(), pygame.SRCALPHA)
dark_overlay.fill((0, 0, 0, 50))

player_pos = pygame.Vector2(175, 340)

floor = pygame.image.load("Assets/floor.png")

lockedDoor = pygame.transform.scale(Assets.lockedDoorNorth, (128,128))
openDoor = pygame.transform.scale(Assets.grayDoorNorth, (128,128)) 

dimLightScale1 = pygame.transform.scale(Assets.squishedDimTiles[3], (Assets.squishedDimTiles[3].get_width()/2, Assets.squishedDimTiles[3].get_height()*1.5))
dimLightScale2 = pygame.transform.scale(Assets.squishedDimTiles[3], (Assets.squishedDimTiles[3].get_width()/2.2, Assets.squishedDimTiles[3].get_height()*1.5))
dimLightScale3 = pygame.transform.scale(Assets.squishedDimTiles[3], (Assets.squishedDimTiles[3].get_width()/2.5, Assets.squishedDimTiles[3].get_height()*1.5))

LightScale1 = pygame.transform.scale(Assets.squishedTiles[3], (Assets.squishedTiles[1].get_width()/2, Assets.squishedTiles[3].get_height()*1.5))
LightScale2 = pygame.transform.scale(Assets.squishedTiles[3], (Assets.squishedTiles[1].get_width()/2.2, Assets.squishedTiles[3].get_height()*1.5))
LightScale3 = pygame.transform.scale(Assets.squishedTiles[3], (Assets.squishedTiles[1].get_width()/2.5, Assets.squishedTiles[3].get_height()*1.5))

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
    doorRect = openDoor.get_rect()
    doorRect.topleft = (112,128)
    if y > 384:
        return 0
    elif doorRect.collidepoint((x,y)):
        return 1
    elif x < 16 or x > 336:
        return False
    elif x < 64:
        if y > 384 - (x + 64):
            return True
        return False
    elif x >= 64 and x < 288:
        if y > 256:
            return True
        return False
    elif x >= 288:
        if y > 384 - (352 - x + 64):
            return True
        return False

def positionDeterminer(cameFrom):
    global player_pos
    player_pos = pygame.Vector2(175, 340)

def Room(screen, screen_res, events):
    global greenPower, played

    # poll for events
    # for event in events:
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_e:

    if powerSoundTimer.Done() and not played:
        played = True
        Sounds.powerOnAmb.play(-1)

    # fill the screen with a color to wipe away anything from last frame
    virtual_screen.fill("gray")
    dark_overlay.fill((0, 0, 0, 150))

    virtual_screen.blit(floor, (0, 256))
    pygame.draw.line(virtual_screen, (0,0,0), (64, 0), (64, 256), 1)
    pygame.draw.line(virtual_screen, (0,0,0), (288, 0), (288, 256), 1)

    level, power = Objects.getPipeDungeonInfo()

    pinkLit = (level == 1 and power) or Objects.getPinkPower()
    blueLit = (level == 2 and power) or Objects.getBluePower()
    greenLit = (level == 3 and power) or Objects.getGreenPower()
    yellowLit = (level == 4 and power)

    for y in range(208, 400, 32):
        virtual_screen.blit(Assets.pipes[7], (160, y))

    if pinkLit and blueLit and greenLit and yellowLit:
        Assets.punch_light_hole(virtual_screen, dark_overlay, (virtual_screen.get_width()/1.8, virtual_screen.get_height()/2), 500, (0, 0, 0))
        virtual_screen.blit(openDoor, (112,128))
    else:
        virtual_screen.blit(lockedDoor, (112,128))

    if pinkLit:
        virtual_screen.blit(Assets.tiles[1], (64,0))
        virtual_screen.blit(Assets.tiles[1], (112,64))
    else:
        virtual_screen.blit(Assets.dimTiles[1], (64,0))
        virtual_screen.blit(Assets.dimTiles[1], (112,64))

    if blueLit:
        virtual_screen.blit(Assets.tiles[2], (256,0))
        virtual_screen.blit(Assets.tiles[2], (144,64))
    else:
        virtual_screen.blit(Assets.dimTiles[2], (256,0))
        virtual_screen.blit(Assets.dimTiles[2], (144,64))

    if greenLit:
        virtual_screen.blit(Assets.tiles[3], (64,224))
        virtual_screen.blit(Assets.tiles[3], (176,64))
        
    else:
        virtual_screen.blit(Assets.dimTiles[3], (64,224))
        virtual_screen.blit(Assets.dimTiles[3], (176,64))

    if yellowLit:
        virtual_screen.blit(Assets.tiles[4], (256,224))
        virtual_screen.blit(Assets.tiles[4], (208,64))
    else:
        virtual_screen.blit(Assets.dimTiles[4], (256,224))
        virtual_screen.blit(Assets.dimTiles[4], (208,64))

    Player.animatePlayer(virtual_screen, player_pos)

    # apply lighting
    if greenPower:
        #LightSource(upperWingLight.x + 16, upperWingLight.y + 16, radius=pinkLightRadius, strength = pinkLightStrength, color = pinkLightColor)
        apply_lighting(virtual_screen, lightsNew, darkness=10, ambient_color=(50, 50, 50), ambient_strength=10)
        # apply falloff
        apply_falloff(falloff, virtual_screen, (lightsNew[0].x, lightsNew[0].y))
        apply_falloff(falloff, virtual_screen, (lightsNew[1].x, lightsNew[1].y))
        apply_falloff(falloff, virtual_screen, (lightsNew[2].x, lightsNew[2].y))
        apply_falloff(falloff, virtual_screen, (lightsNew[3].x, lightsNew[3].y))
        apply_falloff(falloff, virtual_screen, (lightsNew[4].x, lightsNew[4].y))

        lightsNew.pop()

        #for i in range(4, len(lightsNew)):
            #apply_falloff(falloff, virtual_screen, (lightsNew[i].x, lightsNew[i].y))

    virtual_screen.blit(dark_overlay, (0, 0))

    Assets.scaled_draw(virtual_res, virtual_screen, screen_res, screen)

    return player_pos, 2, 2  # can return movement speeds of 2, 2 since room is scaled (can pick any equal values)
